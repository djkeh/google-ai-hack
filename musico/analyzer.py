import base64
from pathlib import Path
from typing import Optional, List
import numpy as np
import librosa

from .config import TRANSCRIBE_MODEL, GEMINI_API_KEY
from .schemas import AudioFeatures, OnsetPoint, CurvePoint, DetectedSection


def _transcribe_audio_optional(audio_path: Path) -> Optional[str]:
    if not GEMINI_API_KEY:
        return None
    try:
        from google import genai

        client = genai.Client(api_key=GEMINI_API_KEY)
        raw_bytes = audio_path.read_bytes()
        # Only attempt inline transcription if reasonable size
        if len(raw_bytes) > 8 * 1024 * 1024:
            return "Instrumental"
        b64_audio = base64.b64encode(raw_bytes).decode("utf-8")
        interaction = client.interactions.create(
            model=TRANSCRIBE_MODEL,
            input=[
                {
                    "type": "text",
                    "text": "Transcribe any sung lyrics in this audio. If instrumental only, reply 'Instrumental'.",
                },
                {"type": "audio", "data": b64_audio, "mime_type": "audio/wav"},
            ],
        )
        txt = (interaction.output_text or "").strip()
        return txt if txt else "Instrumental"
    except Exception:
        return "Instrumental"


def analyze_audio(
    audio_path: Path,
    transcribe_lyrics: bool = False,
    expected_bpm: Optional[float] = None,
) -> AudioFeatures:
    """Extracts BPM, beat grid, onsets with strengths, RMS curve, spectral centroid curve, and sections."""
    y, sr = librosa.load(str(audio_path), sr=22050, mono=True)
    duration = float(librosa.get_duration(y=y, sr=sr))

    # 1. Tempo & Beats
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr, start_bpm=expected_bpm or 120.0)
    if isinstance(tempo, np.ndarray):
        bpm = float(tempo[0]) if tempo.size > 0 else (expected_bpm or 120.0)
    else:
        bpm = float(tempo)
    if bpm < 80.0:
        bpm *= 2.0
    if expected_bpm and abs(bpm - expected_bpm) > 15.0:
        bpm = float(expected_bpm)

    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    beats = [round(float(bt), 4) for bt in beat_times]

    # Ensure beat grid covers full track if beat tracker starts late
    if len(beats) < 8:
        beat_step = 60.0 / bpm
        beats = [round(i * beat_step, 4) for i in range(int(duration / beat_step))]

    # 2. Onset envelope & Onset timestamps + normalized strengths
    hop_length = 512
    onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop_length)
    onset_frames = librosa.onset.onset_detect(
        onset_envelope=onset_env,
        sr=sr,
        hop_length=hop_length,
        backtrack=False,
        delta=0.06,
        wait=4,
    )
    onset_times = librosa.frames_to_time(onset_frames, sr=sr, hop_length=hop_length)
    max_env = float(np.max(onset_env)) if onset_env.size > 0 and np.max(onset_env) > 0 else 1.0

    onsets: List[OnsetPoint] = []
    for frame_idx, t_val in zip(onset_frames, onset_times):
        strength = float(onset_env[min(frame_idx, len(onset_env) - 1)]) / max_env
        onsets.append(
            OnsetPoint(
                t=round(float(t_val), 4),
                strength=round(float(np.clip(strength, 0.05, 1.0)), 3),
            )
        )

    # 3. RMS Energy Curve & Spectral Centroid Curve (sampled at ~10Hz / 0.1s intervals)
    rms_raw = librosa.feature.rms(y=y, hop_length=hop_length)[0]
    cent_raw = librosa.feature.spectral_centroid(y=y, sr=sr, hop_length=hop_length)[0]
    frame_times = librosa.frames_to_time(np.arange(len(rms_raw)), sr=sr, hop_length=hop_length)

    rms_max = float(np.max(rms_raw)) if rms_raw.size > 0 and np.max(rms_raw) > 0 else 1.0
    cent_max = float(np.max(cent_raw)) if cent_raw.size > 0 and np.max(cent_raw) > 0 else 1.0

    rms_norm = rms_raw / rms_max
    cent_norm = cent_raw / cent_max

    sample_grid = np.arange(0.0, duration, 0.1)
    rms_interp = np.interp(sample_grid, frame_times, rms_norm)
    cent_interp = np.interp(sample_grid, frame_times, cent_norm)

    rms_curve = [
        CurvePoint(t=round(float(tg), 2), value=round(float(rv), 4))
        for tg, rv in zip(sample_grid, rms_interp)
    ]
    spectral_centroid_curve = [
        CurvePoint(t=round(float(tg), 2), value=round(float(cv), 4))
        for tg, cv in zip(sample_grid, cent_interp)
    ]

    # 4. Novelty / Agglomerative Section Boundaries (k=4 sections)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, hop_length=hop_length)
    k_sections = 4
    try:
        bound_frames = librosa.segment.agglomerative(mfcc, k=k_sections)
        bound_times = librosa.frames_to_time(bound_frames, sr=sr, hop_length=hop_length)
        boundaries = [0.0] + [round(float(bt), 2) for bt in bound_times[1:]] + [round(duration, 2)]
    except Exception:
        boundaries = [
            0.0,
            round(duration * 0.25, 2),
            round(duration * 0.55, 2),
            round(duration * 0.84, 2),
            round(duration, 2),
        ]

    # Clean up boundaries that are too close (< 3.5s)
    cleaned = [0.0]
    for b in boundaries[1:-1]:
        if b - cleaned[-1] >= 4.0 and (duration - b) >= 3.5:
            cleaned.append(b)
    cleaned.append(round(duration, 2))
    if len(cleaned) < 4:
        cleaned = [
            0.0,
            round(duration * 0.25, 2),
            round(duration * 0.55, 2),
            round(duration * 0.84, 2),
            round(duration, 2),
        ]

    sections_detected: List[DetectedSection] = []
    # Find highest energy section to tag as climax
    sec_energies = []
    for idx in range(len(cleaned) - 1):
        s_t, e_t = cleaned[idx], cleaned[idx + 1]
        mask = (frame_times >= s_t) & (frame_times <= e_t)
        avg_e = float(np.mean(rms_norm[mask])) if np.any(mask) else 0.3
        avg_b = float(np.mean(cent_norm[mask])) if np.any(mask) else 0.3
        sec_energies.append((avg_e, avg_b))

    climax_idx = int(np.argmax([se[0] for se in sec_energies]))
    for idx in range(len(cleaned) - 1):
        s_t, e_t = cleaned[idx], cleaned[idx + 1]
        avg_e, avg_b = sec_energies[idx]
        if idx == 0:
            role = "intro"
        elif idx == climax_idx:
            role = "climax"
        elif idx == len(cleaned) - 2:
            role = "outro"
        else:
            role = "development"
        sections_detected.append(
            DetectedSection(
                index=idx,
                start=s_t,
                end=e_t,
                avg_energy=round(avg_e, 3),
                avg_brightness=round(avg_b, 3),
                suggested_role=role,
            )
        )

    lyrics = _transcribe_audio_optional(audio_path) if transcribe_lyrics else "Instrumental"

    return AudioFeatures(
        filename=audio_path.name,
        duration=round(duration, 2),
        bpm=round(bpm, 1),
        beats=beats,
        onsets=onsets,
        rms_curve=rms_curve,
        spectral_centroid_curve=spectral_centroid_curve,
        sections_detected=sections_detected,
        lyrics=lyrics,
    )
