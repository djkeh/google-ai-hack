from pathlib import Path
from typing import Dict, List, Any
import numpy as np
import soundfile as sf

from .config import DEMO_AUDIO_DIR


DEMO_TRACKS_META: List[Dict[str, Any]] = [
    {
        "track_id": "sugar_plum_fairy",
        "title": "Dance of the Sugar Plum Fairy (Celesta Etude)",
        "genre": "Classical / Chamber Music Box",
        "composer": "P. I. Tchaikovsky (Public Domain Arrangement)",
        "bpm": 120.0,
        "duration": 32.0,
        "filename": "sugar_plum_fairy.wav",
        "default_prompt": (
            "Direct a crystalline Sugar-Plum Fairy in an enchanted violet music-box theater. "
            "Keep the prelude hushed and tiptoeing, leap on the B-section woodwind accents, "
            "and unleash a golden stardust storm during the fortissimo celesta climax."
        ),
    },
    {
        "track_id": "neon_pulse",
        "title": "Neon Pulse (Cyberpunk Etude)",
        "genre": "Electronic / Synthwave",
        "composer": "Lyria-3.5 / Procedural Synth Studio",
        "bpm": 128.0,
        "duration": 32.0,
        "filename": "neon_pulse.wav",
        "default_prompt": (
            "Direct a kinetic Neon Cyber-Dancer on a rain-slicked holographic rooftop. "
            "Sync robotic step-grooves to the 128 BPM arpeggio, build tension with spinning "
            "charge rings during the riser, and trigger high-voltage shockwave leaps on the drop."
        ),
    },
]


def _midi_to_freq(midi_note: float) -> float:
    return 440.0 * (2.0 ** ((midi_note - 69.0) / 12.0))


def _add_celesta_note(
    buf: np.ndarray,
    sr: int,
    start_sec: float,
    dur_sec: float,
    midi_note: float,
    amp: float = 0.25,
    shimmer: float = 0.3,
) -> None:
    i0 = int(start_sec * sr)
    n = int(dur_sec * sr)
    if i0 >= len(buf) or n <= 0:
        return
    i1 = min(len(buf), i0 + n)
    t = np.arange(i1 - i0, dtype=np.float64) / sr
    f0 = _midi_to_freq(midi_note)

    # Crisp mallet attack + warm bell decay
    attack = np.clip(t / 0.006, 0.0, 1.0)
    decay1 = np.exp(-t * 4.5)
    decay2 = np.exp(-t * 11.0)
    decay_bell = np.exp(-t * 18.0)

    tone = (
        0.65 * np.sin(2 * np.pi * f0 * t) * decay1
        + 0.22 * np.sin(2 * np.pi * (2.0 * f0) * t) * decay2
        + 0.10 * np.sin(2 * np.pi * (3.0 * f0) * t) * decay2
        + shimmer * 0.14 * np.sin(2 * np.pi * (5.41 * f0) * t) * decay_bell
    )
    buf[i0:i1] += amp * attack * tone


def _add_pizzicato(
    buf: np.ndarray, sr: int, start_sec: float, midi_note: float, amp: float = 0.22
) -> None:
    dur_sec = 0.28
    i0 = int(start_sec * sr)
    n = int(dur_sec * sr)
    if i0 >= len(buf) or n <= 0:
        return
    i1 = min(len(buf), i0 + n)
    t = np.arange(i1 - i0, dtype=np.float64) / sr
    f0 = _midi_to_freq(midi_note)
    env = np.clip(t / 0.004, 0.0, 1.0) * np.exp(-t * 14.0)
    sig = (
        0.75 * np.sin(2 * np.pi * f0 * t)
        + 0.25 * np.sin(2 * np.pi * 2 * f0 * t) * np.exp(-t * 25.0)
    )
    buf[i0:i1] += amp * env * sig


def _add_string_swell(
    buf: np.ndarray,
    sr: int,
    start_sec: float,
    dur_sec: float,
    midi_notes: List[float],
    amp: float = 0.12,
) -> None:
    i0 = int(start_sec * sr)
    n = int(dur_sec * sr)
    if i0 >= len(buf) or n <= 0:
        return
    i1 = min(len(buf), i0 + n)
    t = np.arange(i1 - i0, dtype=np.float64) / sr
    env = np.sin(np.pi * np.clip(t / dur_sec, 0.0, 1.0)) ** 0.8
    chord = np.zeros_like(t)
    for m in midi_notes:
        f = _midi_to_freq(m)
        vib = 1.0 + 0.0025 * np.sin(2 * np.pi * 5.2 * t)
        chord += np.sin(2 * np.pi * f * vib * t) + 0.3 * np.sin(2 * np.pi * 2 * f * t)
    buf[i0:i1] += amp * env * (chord / max(1, len(midi_notes)))


def synthesize_sugar_plum_fairy(out_path: Path, sr: int = 22050) -> Path:
    """Synthesizes a 32-second Classical / Music-Box arrangement of Dance of the Sugar Plum Fairy."""
    duration = 32.0
    buf = np.zeros(int(duration * sr), dtype=np.float64)
    beat_sec = 0.5  # 120 BPM

    # Section 1 (0.0s - 8.0s): Hushed Pizzicato & Iconic Celesta Melody
    bass_pattern = [52, 59, 64, 59]  # E3, B3, E4, B3
    for beat in range(16):
        t_b = beat * beat_sec
        _add_pizzicato(buf, sr, t_b, bass_pattern[beat % 4], amp=0.18 if beat < 4 else 0.14)

    # Iconic Tchaikovsky motif starting at t=2.0s (Bar 2)
    melody_sec1 = [
        # (t, midi, dur, amp)
        (2.00, 79, 0.25, 0.26),  # G5
        (2.25, 76, 0.25, 0.24),  # E5
        (2.50, 79, 0.45, 0.32),  # G5 accent
        (3.00, 78, 0.45, 0.30),  # F#5
        (3.50, 75, 0.25, 0.25),  # D#5
        (3.75, 76, 0.25, 0.26),  # E5
        (4.00, 74, 0.22, 0.28),  # D5
        (4.25, 74, 0.22, 0.28),  # D5
        (4.50, 74, 0.45, 0.32),  # D5
        (5.00, 73, 0.22, 0.28),  # C#5
        (5.25, 73, 0.22, 0.28),  # C#5
        (5.50, 73, 0.45, 0.32),  # C#5
        (6.00, 72, 0.22, 0.30),  # C5
        (6.25, 72, 0.22, 0.30),  # C5
        (6.50, 72, 0.45, 0.34),  # C5
        (7.00, 71, 0.45, 0.36),  # B4 resolve
        (7.50, 83, 0.45, 0.42),  # High B5 bell cue before B-section
    ]
    for t_note, midi, dur, amp in melody_sec1:
        _add_celesta_note(buf, sr, t_note, dur, midi, amp=amp, shimmer=0.25)

    # Section 2 (8.0s - 18.0s): Rhythmic Staccato B-Section & Cascading Runs
    for beat in range(16, 36):
        t_b = beat * beat_sec
        _add_pizzicato(buf, sr, t_b, 47 if beat % 2 == 0 else 59, amp=0.26)
        if beat % 4 == 0:
            # Strong rhythmic woodwind/bell accent every 2 seconds (8.0, 10.0, 12.0, 14.0, 16.0)
            _add_celesta_note(buf, sr, t_b, 0.45, 84, amp=0.48, shimmer=0.45)
            _add_celesta_note(buf, sr, t_b, 0.45, 72, amp=0.32, shimmer=0.30)
        elif beat % 2 == 1:
            # Playful cascading arpeggio run
            run_notes = [76, 79, 83, 86] if (beat // 2) % 2 == 0 else [78, 81, 84, 88]
            for idx, rn in enumerate(run_notes):
                _add_celesta_note(buf, sr, t_b + idx * 0.125, 0.22, rn, amp=0.30, shimmer=0.35)

    # Pre-climax harp glissando (17.0s - 18.0s)
    gliss_scale = [64, 66, 67, 69, 71, 72, 75, 76, 78, 79, 81, 83, 84, 87, 88, 91]
    for idx, gn in enumerate(gliss_scale):
        _add_celesta_note(buf, sr, 17.0 + idx * (1.0 / len(gliss_scale)), 0.35, gn, amp=0.36, shimmer=0.5)

    # Section 3 (18.0s - 27.0s): Fortissimo Stardust Climax!
    _add_string_swell(buf, sr, 18.0, 4.5, [52, 59, 64, 67, 71], amp=0.26)
    _add_string_swell(buf, sr, 22.5, 4.5, [57, 60, 64, 69, 72], amp=0.28)

    climax_chords = [
        (18.0, [76, 83, 88]),
        (19.0, [79, 86, 91]),
        (20.0, [81, 88, 93]),
        (21.0, [78, 86, 90]),
        (22.0, [83, 91, 95]),
        (23.0, [84, 91, 96]),
        (24.0, [81, 88, 93]),
        (25.0, [79, 87, 91]),
        (26.0, [88, 95, 100]),
    ]
    for t_c, chord_notes in climax_chords:
        _add_pizzicato(buf, sr, t_c, 40, amp=0.45)  # Deep bass pizzicato impact
        for cn in chord_notes:
            _add_celesta_note(buf, sr, t_c, 0.85, cn, amp=0.42, shimmer=0.65)
        # Shimmering 16th-note upper sparkle
        for sub in range(1, 8):
            _add_celesta_note(
                buf,
                sr,
                t_c + sub * 0.125,
                0.20,
                chord_notes[-1] + (3 if sub % 2 == 0 else 0),
                amp=0.26,
                shimmer=0.6,
            )

    # Section 4 (27.0s - 32.0s): Crystalline Music-Box Coda
    coda_notes = [
        (27.0, 88, 0.6, 0.34),
        (27.5, 83, 0.6, 0.30),
        (28.0, 79, 0.6, 0.28),
        (28.5, 76, 0.6, 0.25),
        (29.0, 71, 0.8, 0.24),
        (30.0, 88, 1.8, 0.40),  # Final crystalline E6 chime
        (30.0, 76, 1.8, 0.28),
    ]
    for t_n, midi, dur, amp in coda_notes:
        _add_celesta_note(buf, sr, t_n, dur, midi, amp=amp, shimmer=0.4)

    # Normalize cleanly to -1.0 dBFS
    peak = np.max(np.abs(buf))
    if peak > 0:
        buf = (buf / peak) * 0.89

    out_path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(out_path), buf.astype(np.float32), sr)
    return out_path


def _add_kick(buf: np.ndarray, sr: int, start_sec: float, amp: float = 0.55) -> None:
    dur_sec = 0.24
    i0 = int(start_sec * sr)
    n = int(dur_sec * sr)
    if i0 >= len(buf) or n <= 0:
        return
    i1 = min(len(buf), i0 + n)
    t = np.arange(i1 - i0, dtype=np.float64) / sr
    # Pitch drop from 150Hz to 46Hz
    freq = 46.0 + 110.0 * np.exp(-t * 32.0)
    phase = 2 * np.pi * np.cumsum(freq) / sr
    env = np.exp(-t * 11.5)
    click = 0.25 * np.sin(2 * np.pi * 1200.0 * t) * np.exp(-t * 140.0)
    buf[i0:i1] += amp * (np.sin(phase) * env + click)


def _add_snare(
    buf: np.ndarray, sr: int, start_sec: float, amp: float = 0.40, rng: np.random.Generator = None
) -> None:
    if rng is None:
        rng = np.random.default_rng(42)
    dur_sec = 0.18
    i0 = int(start_sec * sr)
    n = int(dur_sec * sr)
    if i0 >= len(buf) or n <= 0:
        return
    i1 = min(len(buf), i0 + n)
    t = np.arange(i1 - i0, dtype=np.float64) / sr
    body = np.sin(2 * np.pi * 195.0 * t) * np.exp(-t * 28.0)
    noise = rng.standard_normal(len(t)) * np.exp(-t * 19.0)
    buf[i0:i1] += amp * (0.45 * body + 0.55 * noise)


def _add_synth_note(
    buf: np.ndarray,
    sr: int,
    start_sec: float,
    dur_sec: float,
    midi_note: float,
    amp: float = 0.24,
    bright: float = 0.5,
) -> None:
    i0 = int(start_sec * sr)
    n = int(dur_sec * sr)
    if i0 >= len(buf) or n <= 0:
        return
    i1 = min(len(buf), i0 + n)
    t = np.arange(i1 - i0, dtype=np.float64) / sr
    f0 = _midi_to_freq(midi_note)
    env = np.clip(t / 0.008, 0.0, 1.0) * np.exp(-t * 5.0)
    # Detuned supersaw approximation
    sig = (
        0.50 * np.sin(2 * np.pi * f0 * t)
        + 0.30 * np.sin(2 * np.pi * (f0 * 1.006) * t)
        + bright * 0.30 * np.sin(2 * np.pi * (2 * f0) * t)
        + bright * 0.18 * np.sin(2 * np.pi * (3 * f0) * t)
        + bright * 0.12 * np.sin(2 * np.pi * (4 * f0) * t)
    )
    buf[i0:i1] += amp * env * sig


def synthesize_neon_pulse(out_path: Path, sr: int = 22050) -> Path:
    """Synthesizes a 32-second Electronic / Synthwave track at 128 BPM."""
    duration = 32.0
    buf = np.zeros(int(duration * sr), dtype=np.float64)
    rng = np.random.default_rng(2026)
    beat_sec = 60.0 / 128.0  # 0.46875s per beat

    # Section 1 (0.0s - 9.0s): Midnight Grid Arpeggio (19 beats)
    arp_notes = [57, 60, 64, 69, 64, 60, 53, 57, 60, 65, 60, 57]
    for step in range(int(9.0 / (beat_sec / 2))):
        t_s = step * (beat_sec / 2)
        if step % 2 == 0:
            _add_kick(buf, sr, t_s, amp=0.36)
        _add_synth_note(
            buf,
            sr,
            t_s,
            beat_sec * 0.45,
            arp_notes[step % len(arp_notes)],
            amp=0.22,
            bright=0.35,
        )

    # Section 2 (9.0s - 16.875s): Tension Riser & Accelerating Snare Build
    riser_start = 9.0
    riser_end = 16.875
    i0, i1 = int(riser_start * sr), int(riser_end * sr)
    t_r = np.arange(i1 - i0, dtype=np.float64) / sr
    riser_freq = 220.0 * (2.0 ** (2.5 * (t_r / (riser_end - riser_start)) ** 1.5))
    riser_phase = 2 * np.pi * np.cumsum(riser_freq) / sr
    buf[i0:i1] += 0.24 * (t_r / (riser_end - riser_start)) * np.sin(riser_phase)

    # Snare build: quarter notes -> 8th notes -> 16th notes
    t_cur = 9.0
    while t_cur < 16.4:
        progress = (t_cur - 9.0) / 7.4
        step_dur = beat_sec if progress < 0.4 else (beat_sec / 2 if progress < 0.75 else beat_sec / 4)
        _add_snare(buf, sr, t_cur, amp=0.28 + 0.28 * progress, rng=rng)
        _add_synth_note(buf, sr, t_cur, step_dur * 0.8, 69 + int(progress * 12), amp=0.25, bright=0.6)
        t_cur += step_dur

    # Big pre-drop impact at 16.875s (Beat 36)
    drop_start = 36 * beat_sec  # 16.875s

    # Section 3 (16.875s - 27.1875s): Overdrive Neon Drop (Climax!)
    lead_melody = [76, 79, 81, 84, 83, 79, 76, 74, 76, 79, 81, 88, 86, 84, 81, 79]
    for beat_idx in range(36, 58):
        t_b = beat_idx * beat_sec
        _add_kick(buf, sr, t_b, amp=0.65)
        if beat_idx % 2 == 1:
            _add_snare(buf, sr, t_b, amp=0.52, rng=rng)
        # Sub-bass + Lead
        sub_midi = 45 if ((beat_idx - 36) // 4) % 2 == 0 else 41
        _add_synth_note(buf, sr, t_b + beat_sec * 0.5, beat_sec * 0.45, sub_midi, amp=0.42, bright=0.4)
        m_idx = (beat_idx - 36) % len(lead_melody)
        _add_synth_note(buf, sr, t_b, beat_sec * 0.85, lead_melody[m_idx], amp=0.46, bright=0.95)
        _add_synth_note(buf, sr, t_b, beat_sec * 0.85, lead_melody[m_idx] + 12, amp=0.28, bright=1.0)

    # Section 4 (27.1875s - 32.0s): Cybernetic Horizon Outro
    for step in range(10):
        t_o = 58 * beat_sec + step * (beat_sec / 2)
        if t_o < 31.5:
            _add_synth_note(
                buf,
                sr,
                t_o,
                0.45,
                arp_notes[step % len(arp_notes)] + 12,
                amp=0.26 * (1.0 - step / 11.0),
                bright=0.4,
            )

    peak = np.max(np.abs(buf))
    if peak > 0:
        buf = (buf / peak) * 0.90

    out_path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(out_path), buf.astype(np.float32), sr)
    return out_path


def ensure_demo_assets() -> Dict[str, Path]:
    paths: Dict[str, Path] = {}
    spf_path = DEMO_AUDIO_DIR / "sugar_plum_fairy.wav"
    if not spf_path.exists():
        synthesize_sugar_plum_fairy(spf_path)
    paths["sugar_plum_fairy"] = spf_path

    np_path = DEMO_AUDIO_DIR / "neon_pulse.wav"
    if not np_path.exists():
        synthesize_neon_pulse(np_path)
    paths["neon_pulse"] = np_path
    return paths


if __name__ == "__main__":
    generated = ensure_demo_assets()
    for k, p in generated.items():
        print(f"Generated {k}: {p} ({p.stat().st_size} bytes)")
