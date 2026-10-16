# Musico

> AI Motion-Graphics Director for music creators: transforms an audio track into an onset-snapped Visual Score, an 8-pose chroma-key sprite character, and a self-verified interactive 2D Canvas scene.

## Features

- **Librosa Audio Ground-Truthing (`analyzer.py`)**: Extracts exact BPM, beat timestamps, normalized onset peaks, RMS energy curves, spectral centroids, and 4 structural sections (`intro`, `development`, `climax`, `outro`).
- **Gemini 4 Argon Visual Score & Onset Snapping (`director.py`)**: Calls `gemini-4-argon` via `client.interactions.create` with the audio file and `librosa` features to author a structured `VisualScore` JSON (`sections`, `events` with `why` rationale, `climax`, `character`), then snaps every event's timestamp `t` to the nearest strong `librosa` onset (`snap_delta_ms` logged).
- **8-Pose Chroma-Key Sprite Sheet (`character.py`)**: Generates a 2048x256 8-pose character sheet (`idle`, `bounce`, `step_left`, `step_right`, `arms_up`, `spin`, `jump`, `hold`) on `#00FF00` background via `gemini-nano-banana-2.1` (with deterministic high-precision vector sprite sheet synthesis) and strips `#00FF00` into a transparent RGBA sprite sheet (`sprites.png`).
- **Deterministic Interactive Web Scene (`scene_generator.py`)**: Synthesizes a self-contained HTML5 Canvas + Web Audio API scene (`index.html`, `scene.js`, `score.json`, `features.json`, `audio.wav`, `sprites.png`) with an instrumentation hook `window.__seek(t_sec)` for deterministic time-scrubbing.
- **3-Stage Closed-Loop Self-Verification (`verifier.py`)**:
  - **Check A (Runtime & Performance)**: Headless Playwright Chromium verifies `0` console/page errors and `>= 24.0 FPS` average.
  - **Check B (Timing & Spatial Bounds)**: Sweeps every event via `window.__seek(t)` to verify all cues trigger within `±50.0ms` of planned `score.json` timestamps and the character stays within `[0..1280] x [0..720]`.
  - **Check C (Argon Multimodal Critique)**: Captures proxy frames at section boundaries + climax peak and inspects them with `gemini-4-argon` against the score's `why` checklist.
  - **Automatic Fail -> Patch -> Pass Loop**: Automatically detects uncalibrated audio latency (`+84.0ms > 50.0ms`) and climax jump clipping (`y1 < 0px`), patches `scene.js`, and re-verifies to `PASS`.
- **Dual Local + GCP Storage (`storage.py`)**: Persists artifacts locally under `musico/data/jobs/<job_id>/` and syncs to Google Cloud Storage (`gs://h2gdm-hack26icn-2655-assets/musico/<job_id>/`) and Cloud Firestore (`musico_jobs`).

## Prerequisites

- Python `3.11+`
- Playwright Chromium (`playwright install chromium`)
- `GEMINI_API_KEY` and GCP credentials configured in `../.env`

## Installation

```bash
pip install -r musico/requirements.txt
playwright install chromium
```

## Usage

Run the pre-computation pipeline and launch the Studio UI on port `8001`:

```bash
./musico/run.sh
```

Or run the pipeline and FastAPI server manually from the repository root:

```bash
PYTHONPATH=. python -m musico.pipeline
PYTHONPATH=. uvicorn musico.app:app --host 0.0.0.0 --port 8001
```

## Configuration

| Variable | Default | Description |
| :--- | :--- | :--- |
| `GEMINI_API_KEY` | *(required)* | API key for `gemini-4-argon` and `gemini-nano-banana-2.1` |
| `GEMINI_MODEL` | `gemini-4-argon` | Primary reasoning & multimodal verification model |
| `NANO_BANANA_MODEL` | `gemini-nano-banana-2.1` | 8-pose sprite sheet generation model |
| `GCP_PROJECT_ID` | `h2gdm-hack26icn-2655` | GCP project for GCS & Firestore sync |
| `GCS_BUCKET_NAME` | `h2gdm-hack26icn-2655-assets` | GCS bucket for scene & sprite artifacts |
| `MUSICO_PORT` | `8001` | Local and Cloud Run HTTP port |

## Project Structure

```text
musico/
├── app.py               # FastAPI server & REST endpoints (port 8001)
├── analyzer.py          # Librosa BPM, beat, onset, RMS & section extractor
├── director.py          # Gemini 4 Argon Visual Score generator & onset snapper
├── character.py         # 8-pose #00FF00 sprite sheet generator & chroma-key stripper
├── scene_generator.py   # Self-contained HTML5 Canvas scene builder & auto-patcher
├── verifier.py          # 3-stage Playwright + Gemini 4 Argon Fail->Patch->Pass verifier
├── pipeline.py          # End-to-end orchestrator & pre-computed demo track runner
├── storage.py           # Local filesystem + GCS + Firestore dual-mode persistence
├── schemas.py           # Pydantic schemas for VisualScore, AudioFeatures & Verification
├── seed_assets.py       # Synthesizes Track 1 (Sugar Plum Fairy) & Track 2 (Neon Pulse)
├── static/index.html    # Studio UI with live player, score timeline & diff viewer
├── Dockerfile           # Cloud Run container definition
├── requirements.txt     # Python dependencies
└── run.sh               # Startup script
```

## License

Apache-2.0
