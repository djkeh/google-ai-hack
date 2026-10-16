import json
import logging
import math
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFont

from config import VIDEOS_DIR

logger = logging.getLogger("yourdancer.seed_video")

LIMB_COLORS: Dict[str, Tuple[int, int, int]] = {
    "L_arm": (0, 245, 212),    # Cyan (Lane 0 - D)
    "R_arm": (255, 42, 133),   # Magenta (Lane 1 - F)
    "L_leg": (254, 228, 64),   # Amber (Lane 2 - J)
    "R_leg": (168, 85, 247),   # Violet (Lane 3 - K)
    "both": (255, 255, 255),   # White/Gold Chord (Lane 0 + 1)
}

LANE_MAP = {
    "L_arm": [0],
    "R_arm": [1],
    "L_leg": [2],
    "R_leg": [3],
    "both": [0, 1],
}


def build_choreography_spec(video_key: str) -> Dict[str, Any]:
    """Builds deterministic, musically aligned choreography ground-truth + simulated Argon raw timestamps."""
    if video_key == "kpop_electro_groove":
        bpm = 124.0
        beat_sec = 60.0 / bpm  # ~0.48387s
        duration = 35.0
        sections = [
            {
                "start": 0.0,
                "end": round(beat_sec * 18, 3),
                "name": "INTRO GROOVE",
                "energy": 0.58,
                "summary": "Sharp studio count-in with isolated neon arm punches and syncopated foot steps.",
            },
            {
                "start": round(beat_sec * 18, 3),
                "end": round(beat_sec * 36, 3),
                "name": "VERSE BUILD",
                "energy": 0.78,
                "summary": "Alternating whip slashes, body wave holds, and cross-step kicks building tension.",
            },
            {
                "start": round(beat_sec * 36, 3),
                "end": round(beat_sec * 56, 3),
                "name": "CHORUS DROP",
                "energy": 0.96,
                "summary": "High-impact electro drop with double-arm jump freezes, rapid combos, and power stomps.",
            },
            {
                "start": round(beat_sec * 56, 3),
                "end": duration,
                "name": "OUTRO POSE",
                "energy": 0.68,
                "summary": "Controlled glide holds and signature K-Pop ending freeze on the final downbeat.",
            },
        ]
        # Pattern of (beat_index, part, move_type, hold_beats, label, energy, llm_jitter_sec)
        raw_pattern = [
            (2.0, "L_arm", "hit", 0.0, "Left Neon Jab", 0.55, -0.062),
            (4.0, "R_arm", "hit", 0.0, "Right Wrist Snap", 0.58, 0.074),
            (6.0, "L_leg", "hit", 0.0, "Left Heel Stomp", 0.62, -0.048),
            (8.0, "R_leg", "hit", 0.0, "Right Side Kick", 0.65, 0.055),
            (10.0, "both", "hit", 0.0, "Double Chest Pop", 0.72, -0.081),
            (12.0, "L_arm", "hold", 1.5, "Left Arm Wave Hold", 0.68, 0.064),
            (14.0, "R_arm", "hit", 0.0, "Right Slash Cut", 0.70, -0.052),
            (15.0, "L_leg", "hit", 0.0, "Left Cross Step", 0.66, 0.043),
            (16.0, "R_leg", "hit", 0.0, "Right Pivot Tap", 0.69, -0.039),
            (17.0, "both", "hit", 0.0, "Pre-Verse Jump Lock", 0.80, 0.088),
            # Verse Build (18..36)
            (18.0, "L_arm", "hit", 0.0, "Left Shoulder Isolation", 0.74, -0.071),
            (19.0, "R_arm", "hit", 0.0, "Right Forearm Whip", 0.76, 0.058),
            (20.0, "L_leg", "hit", 0.0, "Left Knee Lift", 0.75, -0.044),
            (21.0, "R_leg", "hit", 0.0, "Right Ankle Flick", 0.77, 0.061),
            (22.0, "R_arm", "hold", 1.5, "Right Ribbon Sweep Hold", 0.81, -0.092),
            (24.0, "L_arm", "hit", 0.0, "Left Uppercut Hit", 0.79, 0.047),
            (25.0, "R_leg", "hit", 0.0, "Right Back Slide", 0.76, -0.053),
            (26.0, "L_leg", "hold", 1.5, "Left Leg Glide Hold", 0.82, 0.069),
            (28.0, "both", "hit", 0.0, "Twin Hand Clap Burst", 0.85, -0.077),
            (29.0, "L_arm", "hit", 0.0, "Left Elbow Strike", 0.78, 0.038),
            (30.0, "R_arm", "hit", 0.0, "Right Crown Pose", 0.82, -0.065),
            (31.0, "L_leg", "hit", 0.0, "Left Low Stomp", 0.80, 0.051),
            (32.0, "R_leg", "hit", 0.0, "Right Spin Step", 0.84, -0.049),
            (33.0, "L_arm", "hit", 0.0, "Left Finger Gun", 0.83, 0.072),
            (34.0, "R_arm", "hit", 0.0, "Right Neck Slice", 0.86, -0.058),
            (35.0, "both", "hit", 0.0, "Drop Countdown Jump", 0.92, 0.095),
            # Chorus Drop (36..56)
            (36.0, "both", "hit", 0.0, "Chorus Impact Stomp", 0.98, -0.084),
            (37.0, "L_arm", "hit", 0.0, "Left Laser Punch", 0.91, 0.045),
            (37.5, "R_arm", "hit", 0.0, "Right Counter Whip", 0.93, -0.037),
            (38.0, "L_leg", "hit", 0.0, "Left Bass Kick", 0.94, 0.063),
            (39.0, "R_leg", "hit", 0.0, "Right Shuffle Drop", 0.92, -0.054),
            (40.0, "L_arm", "hold", 1.5, "Left Cyber Wave Hold", 0.95, 0.079),
            (42.0, "R_arm", "hit", 0.0, "Right Blade Slash", 0.94, -0.061),
            (42.5, "L_leg", "hit", 0.0, "Left Syncopated Tap", 0.90, 0.042),
            (43.0, "R_leg", "hit", 0.0, "Right Heel Slam", 0.93, -0.050),
            (44.0, "both", "hit", 0.0, "Full Body X-Jump", 0.99, 0.087),
            (45.0, "L_arm", "hit", 0.0, "Left Hook Snap", 0.91, -0.046),
            (46.0, "R_arm", "hold", 1.5, "Right Halo Spin Hold", 0.95, 0.068),
            (48.0, "L_leg", "hit", 0.0, "Left Power Lunge", 0.93, -0.073),
            (48.5, "R_leg", "hit", 0.0, "Right Quick Switch", 0.91, 0.052),
            (49.0, "L_arm", "hit", 0.0, "Left Chest Hit", 0.92, -0.041),
            (50.0, "R_arm", "hit", 0.0, "Right Shoulder Drop", 0.94, 0.066),
            (51.0, "L_leg", "hit", 0.0, "Left Side Kick", 0.90, -0.057),
            (52.0, "both", "hit", 0.0, "Double Star Freeze", 0.97, 0.083),
            (53.0, "R_leg", "hold", 1.5, "Right Moonwalk Slide Hold", 0.92, -0.069),
            (55.0, "both", "hit", 0.0, "Chorus Climax Slam", 0.99, 0.075),
            # Outro Pose (56..70)
            (56.0, "L_arm", "hit", 0.0, "Left Cool-Down Wave", 0.75, -0.055),
            (58.0, "R_arm", "hit", 0.0, "Right Wrist Flick", 0.72, 0.062),
            (60.0, "L_leg", "hit", 0.0, "Left Slow Stomp", 0.70, -0.048),
            (62.0, "R_leg", "hold", 2.0, "Right Floor Sweep Hold", 0.74, 0.071),
            (65.0, "L_arm", "hit", 0.0, "Left Collar Pop", 0.68, -0.043),
            (66.0, "R_arm", "hit", 0.0, "Right V-Sign Frame", 0.72, 0.054),
            (68.0, "both", "hit", 0.0, "Final Ending Crown Freeze", 0.95, -0.067),
        ]
        title = "K-Pop Electro Groove (Practice Cam)"
        subtitle = "124 BPM · Neon Practice Room · Full 4-Limb Isolation Routine"
        style = "K-Pop Electro Choreography"
    else:
        bpm = 110.0
        beat_sec = 60.0 / bpm  # ~0.54545s
        duration = 35.0
        sections = [
            {
                "start": 0.0,
                "end": round(beat_sec * 16, 3),
                "name": "BOUNCE CYPHER",
                "energy": 0.60,
                "summary": "Heavy 808 boom-bap groove with chest bounces and crisp arm pops.",
            },
            {
                "start": round(beat_sec * 16, 3),
                "end": round(beat_sec * 32, 3),
                "name": "ISOLATION FLOW",
                "energy": 0.79,
                "summary": "Liquid arm wave holds and syncopated street footwork glides.",
            },
            {
                "start": round(beat_sec * 32, 3),
                "end": round(beat_sec * 48, 3),
                "name": "CREW ROUTINE DROP",
                "energy": 0.94,
                "summary": "Full-crew locking routine with double-hand hits, knee stomps, and air freezes.",
            },
            {
                "start": round(beat_sec * 48, 3),
                "end": duration,
                "name": "STREET FINALE",
                "energy": 0.70,
                "summary": "Slow-motion wave hold into final B-boy stance lock.",
            },
        ]
        raw_pattern = [
            (2.0, "R_arm", "hit", 0.0, "Right Boom-Bap Hit", 0.58, 0.068),
            (4.0, "L_arm", "hit", 0.0, "Left Forearm Lock", 0.60, -0.054),
            (6.0, "R_leg", "hit", 0.0, "RightTimber Stomp", 0.64, 0.072),
            (8.0, "L_leg", "hit", 0.0, "Left Heel Pivot", 0.63, -0.049),
            (10.0, "both", "hit", 0.0, "Cypher Double Pop", 0.74, 0.081),
            (12.0, "R_arm", "hold", 1.5, "Right Liquid Wave Hold", 0.71, -0.063),
            (14.0, "L_arm", "hit", 0.0, "Left Wrist Roll", 0.69, 0.045),
            (15.0, "R_leg", "hit", 0.0, "Right Curb Step", 0.72, -0.058),
            # Isolation Flow (16..32)
            (16.0, "L_leg", "hit", 0.0, "Left C-Walk Tap", 0.76, 0.064),
            (17.0, "L_arm", "hit", 0.0, "Left Tutting Angle", 0.78, -0.052),
            (18.0, "R_arm", "hit", 0.0, "Right Tutting Box", 0.80, 0.071),
            (19.0, "L_arm", "hold", 1.5, "Left Arm Snake Hold", 0.82, -0.086),
            (21.0, "R_leg", "hit", 0.0, "Right Kick Out", 0.79, 0.048),
            (22.0, "L_leg", "hold", 1.5, "Left Brooklyn Glide Hold", 0.84, -0.067),
            (24.0, "both", "hit", 0.0, "Double Shoulder Shrug Hit", 0.86, 0.075),
            (25.0, "R_arm", "hit", 0.0, "Right Point Lock", 0.81, -0.043),
            (26.0, "L_arm", "hit", 0.0, "Left Up-Rock Punch", 0.83, 0.059),
            (27.0, "R_leg", "hit", 0.0, "Right Cross Hop", 0.82, -0.051),
            (28.0, "L_leg", "hit", 0.0, "Left Knee Drop", 0.85, 0.066),
            (30.0, "both", "hit", 0.0, "Crew Break Freeze", 0.90, -0.089),
            # Crew Routine Drop (32..48)
            (32.0, "both", "hit", 0.0, "808 Bass Drop Jump", 0.96, 0.078),
            (33.0, "R_arm", "hit", 0.0, "Right Krump Smash", 0.92, -0.047),
            (33.5, "L_arm", "hit", 0.0, "Left Counter Jab", 0.90, 0.053),
            (34.0, "R_leg", "hit", 0.0, "Right Heavy Stomp", 0.94, -0.062),
            (35.0, "L_leg", "hit", 0.0, "Left Sweep Kick", 0.91, 0.044),
            (36.0, "R_arm", "hold", 1.5, "Right Windmill Prep Hold", 0.95, -0.074),
            (38.0, "L_arm", "hit", 0.0, "Left Elbow Lock", 0.92, 0.061),
            (38.5, "R_leg", "hit", 0.0, "Right Quick Tap", 0.89, -0.038),
            (39.0, "L_leg", "hit", 0.0, "Left Heel Spin", 0.93, 0.057),
            (40.0, "both", "hit", 0.0, "Twin Hand Ground Slap", 0.97, -0.082),
            (41.0, "L_arm", "hold", 1.5, "Left Wave Transfer Hold", 0.93, 0.069),
            (43.0, "R_arm", "hit", 0.0, "Right SnapBack Throw", 0.91, -0.049),
            (44.0, "R_leg", "hit", 0.0, "Right Air Step", 0.92, 0.064),
            (45.0, "L_leg", "hit", 0.0, "Left Stomp Bounce", 0.90, -0.055),
            (46.0, "both", "hit", 0.0, "Crew Unison Power Hit", 0.98, 0.085),
            # Street Finale (48..61)
            (48.0, "R_leg", "hold", 2.0, "Right Slow-Mo Slide Hold", 0.78, -0.072),
            (51.0, "L_arm", "hit", 0.0, "Left Chest Tap", 0.72, 0.048),
            (53.0, "R_arm", "hit", 0.0, "Right Salute Lock", 0.74, -0.056),
            (55.0, "L_leg", "hit", 0.0, "Left Wide Stance Step", 0.70, 0.063),
            (57.0, "both", "hold", 1.5, "Double Arm Wave Hold", 0.82, -0.077),
            (60.0, "both", "hit", 0.0, "Final B-Boy Freeze Pose", 0.96, 0.071),
        ]
        title = "Urban Street Choreography (Crew Cam)"
        subtitle = "110 BPM · Underground Crew Studio · Hip-Hop Locking & Wave Routine"
        style = "Urban Street Hip-Hop & Locking"

    moves: List[Dict[str, Any]] = []
    for idx, (beat_idx, part, mtype, hold_beats, label, energy, jitter) in enumerate(raw_pattern):
        exact_t = round(beat_idx * beat_sec, 3)
        raw_t = round(max(0.55, exact_t + jitter), 3)
        exact_end_t = round((beat_idx + hold_beats) * beat_sec, 3) if mtype == "hold" else exact_t
        raw_end_t = round(exact_end_t + (jitter * 0.8), 3) if mtype == "hold" else raw_t
        moves.append(
            {
                "move_id": f"m_{idx + 1:02d}",
                "beat_idx": beat_idx,
                "exact_t": exact_t,
                "raw_t": raw_t,
                "part": part,
                "type": mtype,
                "exact_end_t": exact_end_t,
                "end_t": raw_end_t,
                "label": label,
                "energy": energy,
            }
        )

    return {
        "video_key": video_key,
        "title": title,
        "subtitle": subtitle,
        "choreo_style": style,
        "bpm": bpm,
        "duration": duration,
        "sections": sections,
        "moves": moves,
    }


def synthesize_dance_audio(spec: Dict[str, Any], wav_path: Path) -> Dict[str, Any]:
    """Synthesizes a crisp, beat-locked stereo electronic/hip-hop practice track with sharp transients."""
    sr = 22050
    duration = float(spec["duration"])
    bpm = float(spec["bpm"])
    beat_sec = 60.0 / bpm
    total_samples = int(sr * duration)
    t = np.linspace(0.0, duration, total_samples, endpoint=False)

    audio = np.zeros(total_samples, dtype=np.float32)

    # 1. Sub-bass & chord progression locked to beats
    is_kpop = spec["video_key"] == "kpop_electro_groove"
    root_freqs = [110.0, 87.31, 130.81, 98.0] if is_kpop else [73.42, 65.41, 82.41, 73.42]

    num_beats = int(duration / beat_sec) + 1
    for b in range(num_beats):
        bt = b * beat_sec
        idx0 = int(bt * sr)
        if idx0 >= total_samples:
            break

        # Kick on every beat (stronger on downbeats)
        kick_len = min(int(0.22 * sr), total_samples - idx0)
        kt = np.linspace(0.0, kick_len / sr, kick_len, endpoint=False)
        freq_env = 145.0 * np.exp(-kt * 28.0) + (55.0 if is_kpop else 48.0)
        phase = 2.0 * np.pi * np.cumsum(freq_env) / sr
        kick_env = np.exp(-kt * 14.0)
        click = np.exp(-kt * 160.0) * 0.65
        audio[idx0 : idx0 + kick_len] += (np.sin(phase) * kick_env * 0.85 + click).astype(np.float32)

        # Snare / Clap on beats 1 and 3 of each 4-beat bar
        if b % 2 == 1:
            sn_len = min(int(0.18 * sr), total_samples - idx0)
            st = np.linspace(0.0, sn_len / sr, sn_len, endpoint=False)
            rng = np.random.default_rng(1000 + b)
            noise = rng.standard_normal(sn_len).astype(np.float32)
            sn_body = np.sin(2.0 * np.pi * 195.0 * st) * np.exp(-st * 25.0)
            sn_env = np.exp(-st * 20.0)
            audio[idx0 : idx0 + sn_len] += (noise * sn_env * 0.55 + sn_body * 0.45).astype(np.float32)

        # 8th-note hi-hat
        half_idx = int((bt + 0.5 * beat_sec) * sr)
        if half_idx < total_samples:
            hh_len = min(int(0.07 * sr), total_samples - half_idx)
            ht = np.linspace(0.0, hh_len / sr, hh_len, endpoint=False)
            rng = np.random.default_rng(5000 + b)
            hh_noise = rng.standard_normal(hh_len).astype(np.float32) * np.exp(-ht * 55.0)
            audio[half_idx : half_idx + hh_len] += hh_noise * 0.28

        # Synth bass note with sidechain pump
        bar_idx = (b // 4) % len(root_freqs)
        f0 = root_freqs[bar_idx]
        b_len = min(int(beat_sec * sr), total_samples - idx0)
        bt_arr = np.linspace(0.0, b_len / sr, b_len, endpoint=False)
        sidechain = 1.0 - 0.75 * np.exp(-bt_arr * 12.0)
        saw = 0.5 * np.sin(2.0 * np.pi * f0 * bt_arr) + 0.3 * np.sin(2.0 * np.pi * (f0 * 2.0) * bt_arr)
        audio[idx0 : idx0 + b_len] += (saw * sidechain * 0.30).astype(np.float32)

    # 2. Add distinct melodic synth stabs & percussive clicks on every choreographed move exact_t
    limb_freqs = {
        "L_arm": 523.25,  # C5
        "R_arm": 659.25,  # E5
        "L_leg": 392.00,  # G4
        "R_leg": 440.00,  # A4
        "both": 783.99,   # G5
    }
    for mv in spec["moves"]:
        mt = float(mv["exact_t"])
        idx0 = int(mt * sr)
        if idx0 >= total_samples:
            continue
        f_lead = limb_freqs.get(mv["part"], 523.25)
        if mv["type"] == "hold":
            dur = max(0.25, float(mv["exact_end_t"]) - mt)
            h_len = min(int(dur * sr), total_samples - idx0)
            ht = np.linspace(0.0, h_len / sr, h_len, endpoint=False)
            vibrato = np.sin(2.0 * np.pi * 6.0 * ht) * 4.0
            lead = np.sin(2.0 * np.pi * (f_lead + vibrato) * ht) * np.exp(-ht * 1.8)
            transient = np.exp(-ht * 140.0) * 0.6
            audio[idx0 : idx0 + h_len] += (lead * 0.32 + transient).astype(np.float32)
        else:
            s_len = min(int(0.14 * sr), total_samples - idx0)
            st = np.linspace(0.0, s_len / sr, s_len, endpoint=False)
            stab = (
                np.sin(2.0 * np.pi * f_lead * st)
                + 0.5 * np.sin(2.0 * np.pi * (f_lead * 1.5) * st)
            ) * np.exp(-st * 22.0)
            transient = np.exp(-st * 150.0) * 0.65
            audio[idx0 : idx0 + s_len] += (stab * 0.35 + transient).astype(np.float32)

    # Normalize cleanly
    peak = float(np.max(np.abs(audio))) or 1.0
    audio = (audio / peak * 0.88).astype(np.float32)
    stereo = np.column_stack([audio, audio])
    sf.write(str(wav_path), stereo, sr)
    return {"sample_rate": sr, "duration": duration, "wav_path": str(wav_path)}


def _draw_dancer_frame(
    draw: ImageDraw.ImageDraw,
    w: int,
    h: int,
    t: float,
    bpm: float,
    active_move: Dict[str, Any] | None,
    move_phase: float,
    section_name: str,
    title: str,
) -> None:
    """Draws the dance studio background, mirror grid, articulated neon dancer, and limb HUD overlays."""
    beat_pos = (t * (bpm / 60.0)) % 1.0
    beat_pulse = math.exp(-beat_pos * 5.0)

    # Studio background & floor perspective grid
    floor_y = int(h * 0.74)
    draw.rectangle([(0, 0), (w, floor_y)], fill=(12, 14, 26))
    draw.rectangle([(0, floor_y), (w, h)], fill=(18, 20, 36))

    # Top LED studio light bar pulsing on beat
    led_val = int(45 + 110 * beat_pulse)
    draw.rectangle([(40, 28), (w - 40, 34)], fill=(0, led_val, int(led_val * 1.2)))

    # Mirror vertical panels
    for mx in range(80, w, 120):
        draw.line([(mx, 34), (mx, floor_y)], fill=(28, 34, 56), width=1)
    draw.line([(0, floor_y), (w, floor_y)], fill=(65, 85, 135), width=2)

    # Perspective floor lines
    cx = w // 2
    for offset in range(-360, 361, 60):
        draw.line([(cx + offset // 3, floor_y), (cx + offset, h)], fill=(32, 42, 72), width=1)

    # Dancer center & bounce
    bounce = math.sin(t * (bpm / 60.0) * math.pi * 2.0) * 6.0
    part = active_move["part"] if active_move else None
    mtype = active_move["type"] if active_move else "hit"
    intensity = math.sin(min(1.0, max(0.0, move_phase)) * math.pi) if active_move else 0.0

    jump_offset = -28.0 * intensity if part == "both" else 0.0
    hip_x = cx
    hip_y = int(floor_y - 92 + bounce * 0.6 + jump_offset)
    neck_x = cx
    neck_y = hip_y - 68

    # Default limb joint positions
    l_shoulder = (neck_x - 24, neck_y + 8)
    r_shoulder = (neck_x + 24, neck_y + 8)
    l_hip = (hip_x - 16, hip_y)
    r_hip = (hip_x + 16, hip_y)

    # Animated joint targets based on active limb move
    if part in ("L_arm", "both"):
        wave = math.sin(move_phase * math.pi * 4.0) * 14.0 if mtype == "hold" else 0.0
        l_elbow = (int(l_shoulder[0] - 34 - 16 * intensity), int(l_shoulder[1] - 12 - 22 * intensity + wave))
        l_hand = (int(l_elbow[0] - 32 - 20 * intensity), int(l_elbow[1] - 26 * intensity - wave))
    else:
        l_elbow = (int(l_shoulder[0] - 22), int(l_shoulder[1] + 24 + bounce * 0.4))
        l_hand = (int(l_elbow[0] - 10), int(l_elbow[1] + 24))

    if part in ("R_arm", "both"):
        wave = math.cos(move_phase * math.pi * 4.0) * 14.0 if mtype == "hold" else 0.0
        r_elbow = (int(r_shoulder[0] + 34 + 16 * intensity), int(r_shoulder[1] - 12 - 22 * intensity + wave))
        r_hand = (int(r_elbow[0] + 32 + 20 * intensity), int(r_elbow[1] - 26 * intensity - wave))
    else:
        r_elbow = (int(r_shoulder[0] + 22), int(r_shoulder[1] + 24 + bounce * 0.4))
        r_hand = (int(r_elbow[0] + 10), int(r_elbow[1] + 24))

    if part in ("L_leg", "both"):
        slide = 24.0 * intensity if mtype == "hold" else 18.0 * intensity
        l_knee = (int(l_hip[0] - 18 - slide), int(l_hip[1] + 42 - 14 * intensity))
        l_foot = (int(l_knee[0] - 18 - slide * 0.8), int(floor_y - 6 - 22 * intensity))
    else:
        l_knee = (int(l_hip[0] - 12), int(l_hip[1] + 46))
        l_foot = (int(l_hip[0] - 18), int(floor_y - 4))

    if part in ("R_leg", "both"):
        slide = 24.0 * intensity if mtype == "hold" else 18.0 * intensity
        r_knee = (int(r_hip[0] + 18 + slide), int(r_hip[1] + 42 - 14 * intensity))
        r_foot = (int(r_knee[0] + 18 + slide * 0.8), int(floor_y - 6 - 22 * intensity))
    else:
        r_knee = (int(r_hip[0] + 12), int(r_hip[1] + 46))
        r_foot = (int(r_hip[0] + 18), int(floor_y - 4))

    # Draw shadow on floor
    draw.ellipse([(cx - 48, floor_y - 8), (cx + 48, floor_y + 10)], fill=(10, 12, 22))

    # Torso & Head
    torso_color = (220, 230, 255) if part == "both" else (140, 165, 220)
    draw.polygon([l_shoulder, r_shoulder, r_hip, l_hip], fill=(35, 48, 82), outline=torso_color)
    head_r = 18
    head_cy = neck_y - 22
    draw.ellipse([(neck_x - head_r, head_cy - head_r), (neck_x + head_r, head_cy + head_r)], fill=(45, 60, 105), outline=torso_color, width=3)

    # Limb colors
    c_l_arm = LIMB_COLORS["L_arm"] if part in ("L_arm", "both") else (70, 145, 155)
    c_r_arm = LIMB_COLORS["R_arm"] if part in ("R_arm", "both") else (155, 70, 115)
    c_l_leg = LIMB_COLORS["L_leg"] if part in ("L_leg", "both") else (155, 145, 75)
    c_r_leg = LIMB_COLORS["R_leg"] if part in ("R_leg", "both") else (120, 85, 165)

    # Legs
    draw.line([l_hip, l_knee, l_foot], fill=c_l_leg, width=9 if part in ("L_leg", "both") else 6)
    draw.line([r_hip, r_knee, r_foot], fill=c_r_leg, width=9 if part in ("R_leg", "both") else 6)
    # Arms
    draw.line([l_shoulder, l_elbow, l_hand], fill=c_l_arm, width=9 if part in ("L_arm", "both") else 6)
    draw.line([r_shoulder, r_elbow, r_hand], fill=c_r_arm, width=9 if part in ("R_arm", "both") else 6)

    # Impact rings on active limb end-effector
    if active_move and intensity > 0.15:
        ring_r = int(12 + 26 * intensity)
        effectors = []
        if part == "L_arm":
            effectors = [(l_hand, LIMB_COLORS["L_arm"])]
        elif part == "R_arm":
            effectors = [(r_hand, LIMB_COLORS["R_arm"])]
        elif part == "L_leg":
            effectors = [(l_foot, LIMB_COLORS["L_leg"])]
        elif part == "R_leg":
            effectors = [(r_foot, LIMB_COLORS["R_leg"])]
        elif part == "both":
            effectors = [(l_hand, LIMB_COLORS["L_arm"]), (r_hand, LIMB_COLORS["R_arm"])]

        for (ex, ey), col in effectors:
            draw.ellipse([(ex - ring_r, ey - ring_r), (ex + ring_r, ey + ring_r)], outline=col, width=3)
            draw.ellipse([(ex - 7, ey - 7), (ex + 7, ey + 7)], fill=col)

    # Top Studio HUD
    draw.rectangle([(12, 8), (w - 12, 26)], fill=(8, 10, 18))
    draw.text((18, 10), f"{title}  |  {int(bpm)} BPM  |  {section_name}", fill=(180, 205, 255))
    draw.text((w - 115, 10), f"TC 00:{t:05.2f}", fill=(0, 245, 212))

    # Active move callout banner for clear visual verification
    if active_move:
        col = LIMB_COLORS.get(part or "both", (255, 255, 255))
        badge_text = f"[{part.upper()} · {mtype.upper()}] {active_move['label']}"
        draw.rectangle([(16, h - 54), (390, h - 22)], fill=(14, 18, 32), outline=col, width=2)
        draw.text((26, h - 44), badge_text, fill=col)

    # Lane Legend on bottom right
    lanes_info = [("D:L_ARM", LIMB_COLORS["L_arm"], "L_arm"), ("F:R_ARM", LIMB_COLORS["R_arm"], "R_arm"), ("J:L_LEG", LIMB_COLORS["L_leg"], "L_leg"), ("K:R_LEG", LIMB_COLORS["R_leg"], "R_leg")]
    lx = w - 235
    for tag, col, p_key in lanes_info:
        is_lit = part == p_key or (part == "both" and p_key in ("L_arm", "R_arm"))
        bg = col if is_lit else (22, 26, 44)
        fg = (10, 12, 20) if is_lit else col
        draw.rectangle([(lx, h - 48), (lx + 52, h - 24)], fill=bg, outline=col, width=1)
        draw.text((lx + 4, h - 41), tag, fill=fg)
        lx += 56


def render_dance_video(spec: Dict[str, Any], wav_path: Path, mp4_path: Path) -> Path:
    """Renders 640x360 @ 24fps H.264 MP4 video with AAC audio via ffmpeg pipe."""
    w, h, fps = 640, 360, 24
    duration = float(spec["duration"])
    total_frames = int(duration * fps)
    bpm = float(spec["bpm"])
    moves = spec["moves"]
    sections = spec["sections"]

    cmd = [
        "ffmpeg",
        "-y",
        "-f",
        "rawvideo",
        "-vcodec",
        "rawvideo",
        "-s",
        f"{w}x{h}",
        "-pix_fmt",
        "rgb24",
        "-r",
        str(fps),
        "-i",
        "-",
        "-i",
        str(wav_path),
        "-c:v",
        "libx264",
        "-preset",
        "ultrafast",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        "160k",
        "-shortest",
        "-movflags",
        "+faststart",
        str(mp4_path),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    assert proc.stdin is not None

    for f_idx in range(total_frames):
        t = f_idx / fps
        sec_name = "PRACTICE"
        for s in sections:
            if s["start"] <= t <= s["end"]:
                sec_name = s["name"]
                break

        active_mv = None
        move_phase = 0.0
        for mv in moves:
            mt = float(mv["exact_t"])
            mend = float(mv["exact_end_t"]) if mv["type"] == "hold" else mt + 0.28
            if mt - 0.08 <= t <= mend + 0.08:
                active_mv = mv
                span = max(0.15, (mend + 0.08) - (mt - 0.08))
                move_phase = (t - (mt - 0.08)) / span
                break

        img = Image.new("RGB", (w, h), (12, 14, 26))
        draw = ImageDraw.Draw(img)
        _draw_dancer_frame(draw, w, h, t, bpm, active_mv, move_phase, sec_name, spec["title"])
        proc.stdin.write(img.tobytes())

    proc.stdin.close()
    stderr_bytes = proc.stderr.read() if proc.stderr else b""
    ret = proc.wait()
    if ret != 0:
        raise RuntimeError(f"ffmpeg failed ({ret}): {stderr_bytes.decode('utf-8', errors='ignore')[-500:]}")
    return mp4_path


def ensure_seed_videos() -> Dict[str, Dict[str, Any]]:
    """Ensures both copyright-safe 35s demo dance videos and their ground-truth specs exist on disk."""
    results: Dict[str, Dict[str, Any]] = {}
    for key in ("kpop_electro_groove", "urban_street_choreo"):
        spec = build_choreography_spec(key)
        wav_path = VIDEOS_DIR / f"{key}.wav"
        mp4_path = VIDEOS_DIR / f"{key}.mp4"
        spec_path = VIDEOS_DIR / f"{key}_spec.json"

        if not wav_path.exists() or not mp4_path.exists() or not spec_path.exists():
            logger.info("Generating demo dance video + audio for %s...", key)
            synthesize_dance_audio(spec, wav_path)
            render_dance_video(spec, wav_path, mp4_path)
            spec_path.write_text(json.dumps(spec, indent=2, ensure_ascii=False), encoding="utf-8")

        spec["wav_path"] = str(wav_path)
        spec["mp4_path"] = str(mp4_path)
        spec["spec_path"] = str(spec_path)
        results[key] = spec
    return results


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    out = ensure_seed_videos()
    for k, v in out.items():
        print(f"Generated {k}: {v['mp4_path']} ({len(v['moves'])} moves, {v['bpm']} BPM)")
