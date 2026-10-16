# YourDancer — AI Dance Practice Video to Playable 4-Lane Rhythm Game

**Multimodal video choreography extraction (`gemini-4-argon`) + Librosa audio onset snapping + self-verifying 3-difficulty HTML5 Canvas rhythm game.**

[![Track 1: Creative Multimodal](https://img.shields.io/badge/Track_1-Creative_Multimodal-00f5d4?style=flat-square)](#)
[![Model: Gemini 4 Argon](https://img.shields.io/badge/Model-gemini--4--argon-ff2a85?style=flat-square)](#)
[![Audio DSP: Librosa](https://img.shields.io/badge/Audio_DSP-Librosa_Onset_Snap-fee440?style=flat-square)](#)
[![Verification: Playwright Auto-Player](https://img.shields.io/badge/Verification-100%25_Auto--Player_PASS-10b981?style=flat-square)](#)

---

## Overview

Dancers practicing to choreography videos frequently struggle to lock limb isolations (`Left Arm`, `Right Arm`, `Left Leg`, `Right Leg`, `Full-Body Lock`) to exact musical transients. Conversely, rhythm game players want playable charts generated directly from real dance videos—not random beat-finders disconnected from the physical choreography.

**YourDancer** bridges both worlds:
1. **Multimodal Video Scrubbing (`gemini-4-argon`, `thinking_level="high"`)**: Uploads the dance video via the Gemini Files API (`client.files.upload`) and invokes the Interactions API (`client.interactions.create`) to extract distinct physical limb moves (`part`, `type: hit|hold`, `raw_t`, `end_t`, `label`, `energy`) alongside choreographer coaching notes and phrase breakdowns.
2. **Audio Onset & Beat-Grid Snapping (`librosa`)**: Because video frame timestamps (`24–30 fps`) have `±40–90ms` visual jitter relative to musical transients, `snapper.py` extracts the audio onset envelope (`librosa.onset.onset_detect` + `librosa.beat.beat_track`) and snaps every `raw_t` to its nearest physical audio transient (`snapped_t`), logging exact snap distances in milliseconds.
3. **4-Lane Limb Mapping & 3-Difficulty Chart Generation**:
   - **Lane 0 (`D`)**: Left Arm (`L_arm`)
   - **Lane 1 (`F`)**: Right Arm (`R_arm`)
   - **Lane 2 (`J`)**: Left Leg (`L_leg`)
   - **Lane 3 (`K`)**: Right Leg (`R_leg`)
   - **Lanes 0+1 (`D+F`)**: Simultaneous Full-Body Lock (`both`)
4. **Closed-Loop Verification (`Fail -> Patch -> Pass` + Headless Playwright Auto-Player)**:
   - **Signal 1 (`validator.py`)**: Enforces 4 playability rules across `Easy`, `Normal`, and `Hard` (no same-lane notes `< 80ms`, 1.0s sliding window NPS caps `Easy<=2 / Normal<=4 / Hard<=7`, no overlapping hold notes + `50ms` release buffer, valid duration bounds). Iteration 1 catches raw chart violations (`12 violations`), applies automated DSP + Argon repair, and passes 100% (`0 violations`) on Iteration 2.
   - **Signal 2 (`verifier.py`)**: Launches headless Chromium via Playwright, injects exact note hit/release timestamps into `window.__runAutoPlayer("perfect")`, asserts **100.0% Perfect accuracy** across all 3 difficulties (`0` console errors), and verifies negative-control failure (`0.0%` accuracy / `100% Miss`) on `+120ms` jittered inputs.

---

## Architecture

```
Dance Practice Video (.mp4)
   │
   ├──► [1. extractor.py] Gemini Files API + gemini-4-argon (thinking_level="high")
   │        Extracts Limb Moves (L_arm, R_arm, L_leg, R_leg, both | hit/hold | raw_t)
   │
   ├──► [2. snapper.py] Librosa Audio Onset & Beat Grid Snapping
   │        Snaps raw_t -> snapped_t within ±110ms window (Mean Δ ~52ms)
   │
   ├──► [3. chart_builder.py + validator.py] Signal 1 Playability Loop
   │        Iteration 1 (FAIL: 12 violations) ──► Automated Patch ──► Iteration 2 (PASS: 0 violations)
   │
   ├──► [4. game_generator.py] Multi-File HTML5 Canvas Rhythm Game
   │        Generates index.html, game.js, judge.js, chart.json, video.mp4
   │
   ├──► [5. verifier.py] Signal 2 Headless Playwright Auto-Player
   │        window.__runAutoPlayer("perfect") -> 100.0% Accuracy | "jitter_120ms" -> 0.0% Accuracy
   │
   └──► [6. storage.py] Dual-Mode Storage
            Local data/jobs/<job_id>/ + Cloud Firestore (yourdancer_jobs) + GCS Bucket
```

---

## Quick Start

### 1. Prerequisites
- Python `3.11+` (shared virtualenv at `/Users/uno/Documents/github/google-ai-hack/.venv`)
- `ffmpeg` installed on `PATH`
- Playwright Chromium installed (`playwright install chromium`)
- `.env` configured with `GEMINI_API_KEY` and GCP credentials

### 2. Run the Studio Server (Port `8002`)

```bash
cd /Users/uno/Documents/github/google-ai-hack/yourdancer
chmod +x run.sh
./run.sh
```

Then open **http://127.0.0.1:8002** in your browser.

### 3. Re-Run the Precomputation & Verification Pipeline Manually

```bash
/Users/uno/Documents/github/google-ai-hack/.venv/bin/python pipeline.py
```

---

## API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Serves the YourDancer Studio Web UI (`static/index.html`) |
| `GET` | `/api/health` | Health check returning active Gemini models, GCP project, and ready job count |
| `GET` | `/api/jobs` | Lists all precomputed and custom choreography jobs with verification badges |
| `GET` | `/api/jobs/{job_id}` | Full job artifact including `snapped_moves`, `snap_stats`, and `verification` logs |
| `POST` | `/api/jobs/{job_id}/reverify` | Runs Signal 1 (Python Validator) + Signal 2 (Headless Playwright Auto-Player) live in ~3s |
| `POST` | `/api/jobs/upload` | Starts a background conversion pipeline for an uploaded MP4 or studio camera preset |
| `GET` | `/jobs/{job_id}/game/index.html` | Standalone playable multi-file 4-lane HTML5 Canvas rhythm game |

---

## Project Structure

```
yourdancer/
├── app.py               # FastAPI server on port 8002 + live re-verification & upload endpoints
├── config.py            # Environment & model configuration (gemini-4-argon, GCP settings)
├── storage.py           # Dual-mode storage (Local JSON + Firestore `yourdancer_jobs` + GCS sync)
├── seed_video.py        # Synthesizes two 35s 640x360 @ 24fps H.264 dance practice videos + WAV audio
├── extractor.py         # Gemini Files API upload + gemini-4-argon structured limb move extraction
├── snapper.py           # Librosa onset_detect + beat_track timestamp snapping (raw_t -> snapped_t)
├── validator.py         # Signal 1: 4-rule Python chart playability validator & auto-patcher
├── chart_builder.py     # Compiles Easy/Normal/Hard charts & orchestrates Fail -> Patch -> Pass loop
├── game_generator.py    # Emits multi-file HTML5 Canvas game (index.html, game.js, judge.js, chart.json)
├── verifier.py          # Signal 2: Headless Playwright Auto-Player (100% Perfect + 120ms Jitter test)
├── pipeline.py          # End-to-end 6-stage orchestrator
├── static/
│   └── index.html       # YourDancer Studio Web UI
├── data/
│   ├── videos/          # Seed MP4 dance practice videos + ground-truth choreography JSON
│   └── jobs/            # Generated game bundles, screenshots, and verification logs
├── requirements.txt
├── Dockerfile
└── run.sh
```
