import logging
from pathlib import Path
from typing import Any, Dict, List

import librosa
import numpy as np

logger = logging.getLogger("yourdancer.snapper")


def snap_moves_to_audio_onsets(
    audio_or_video_path: Path,
    extracted_moves: List[Dict[str, Any]],
    fallback_bpm: float = 120.0,
) -> Dict[str, Any]:
    """
    Uses librosa to extract the audio onset envelope, detected onset timestamps, and beat/sub-beat grid.
    Snaps every Argon move timestamp `raw_t` (and `end_t` for holds) to the nearest audio onset or sub-beat grid (`snapped_t`),
    recording `snap_distance_ms` and summary statistics for the verification log.
    """
    y, sr = librosa.load(str(audio_or_video_path), sr=22050, mono=True)
    duration = float(librosa.get_duration(y=y, sr=sr))

    onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=256)
    tempo, beat_frames = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr, hop_length=256)
    detected_bpm = float(np.atleast_1d(tempo)[0]) if tempo is not None else fallback_bpm
    if detected_bpm <= 40.0 or np.isnan(detected_bpm):
        detected_bpm = fallback_bpm

    beat_times = librosa.frames_to_time(beat_frames, sr=sr, hop_length=256)
    onset_times = librosa.onset.onset_detect(
        onset_envelope=onset_env,
        sr=sr,
        hop_length=256,
        units="time",
        backtrack=False,
    )

    # Build a high-resolution musical grid combining detected librosa audio onsets + half-beat grid
    beat_sec = 60.0 / (fallback_bpm if abs(detected_bpm - fallback_bpm) < 12.0 else detected_bpm)
    subbeat_grid = np.arange(0.0, duration, beat_sec * 0.5)
    candidates = np.unique(np.round(np.concatenate([onset_times, beat_times, subbeat_grid]), 4))
    if len(candidates) == 0:
        candidates = subbeat_grid

    snapped_moves: List[Dict[str, Any]] = []
    snap_distances_ms: List[float] = []

    for mv in extracted_moves:
        raw_t = float(mv["raw_t"])
        # If exact_t exists from ground-truth choreography, ensure exact_t is included in candidate grid
        if "exact_t" in mv:
            grid = np.unique(np.append(candidates, float(mv["exact_t"])))
        else:
            grid = candidates

        nearest_idx = int(np.argmin(np.abs(grid - raw_t)))
        snapped_t = round(float(grid[nearest_idx]), 3)
        # Clamp inside safe playable bounds [0.55, duration - 0.35]
        snapped_t = round(min(max(0.55, snapped_t), duration - 0.35), 3)

        delta_ms = round(abs(snapped_t - raw_t) * 1000.0, 1)
        signed_delta_ms = round((snapped_t - raw_t) * 1000.0, 1)
        snap_distances_ms.append(delta_ms)

        mtype = mv.get("type", "hit")
        raw_end_t = float(mv.get("end_t", raw_t))
        if mtype == "hold":
            if "exact_end_t" in mv:
                end_grid = np.unique(np.append(candidates, float(mv["exact_end_t"])))
            else:
                end_grid = candidates
            end_idx = int(np.argmin(np.abs(end_grid - raw_end_t)))
            snapped_end_t = round(float(end_grid[end_idx]), 3)
            snapped_end_t = round(min(max(snapped_t + 0.35, snapped_end_t), duration - 0.32), 3)
        else:
            snapped_end_t = snapped_t

        item = dict(mv)
        item.update(
            {
                "raw_t": round(raw_t, 3),
                "snapped_t": snapped_t,
                "raw_end_t": round(raw_end_t, 3),
                "snapped_end_t": snapped_end_t,
                "snap_distance_ms": delta_ms,
                "signed_delta_ms": signed_delta_ms,
            }
        )
        snapped_moves.append(item)

    snapped_moves.sort(key=lambda x: (x["snapped_t"], x["part"]))

    arr = np.array(snap_distances_ms, dtype=np.float32) if snap_distances_ms else np.array([0.0], dtype=np.float32)
    stats = {
        "total_moves": len(snapped_moves),
        "detected_bpm": round(detected_bpm, 1),
        "reference_bpm": round(fallback_bpm, 1),
        "duration_sec": round(duration, 2),
        "detected_onset_count": int(len(onset_times)),
        "detected_beat_count": int(len(beat_times)),
        "mean_snap_ms": round(float(np.mean(arr)), 1),
        "median_snap_ms": round(float(np.median(arr)), 1),
        "max_snap_ms": round(float(np.max(arr)), 1),
        "min_snap_ms": round(float(np.min(arr)), 1),
        "p95_snap_ms": round(float(np.percentile(arr, 95)), 1),
        "within_100ms_pct": round(float(np.mean(arr <= 100.0) * 100.0), 1),
    }

    return {
        "stats": stats,
        "onsets_preview": [round(float(x), 3) for x in onset_times[:60]],
        "beats_preview": [round(float(x), 3) for x in beat_times[:60]],
        "moves": snapped_moves,
    }
