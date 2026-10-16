# AGENTS.md — 2026 Google Hackathon (4-Hour Sprint)

## 1. Hackathon Constraints & Golden Rules (4-Hour Timebox)
- **Total Time Limit**: 4 hours (compressed from original 9-hour plan).
- **Execution Mode**: Parallel prototyping across 3 tracks:
  - **Project A — `musico/` (formerly Choreograph)** — Track 1: AI Motion-Graphics Director (Audio -> Visual Score -> 2D Sprite/Canvas Scene -> Self-Verification Loop)
  - **Project B — `yourdancer/` (formerly MoveChart)** — Track 1: Dance Video to Playable 4-Lane Rhythm Game (Video -> Limb Moves + Librosa Onset Snap -> Chart Rule Check + Auto-Player Loop)
  - **Project C — `reprofix/`** — Track 4: Raw Bug Screen Recording to Red-then-Green Pull Request (Video -> Repro Steps -> Failing Playwright Test -> Patch -> Green -> PR)
- **Live Demo Critical Path (< 3 mins)**:
  - Never put 5–10 minute renders or slow full-video passes on the blocking live demo path without a pre-computed/cached instant demo mode AND a fast live verification step.
  - Every project MUST produce at least **1 concrete Fail -> Patch -> Pass verification log** visible in the UI dashboard.

## 2. Gemini 4 Argon & Companion Model Rules
- **SDK**: `google-genai >= 2.30.1`
- **Available Models Verified on API Key**:
  - `gemini-4-argon` (Primary reasoning, long decode, multimodal orchestration)
  - `gemini-3.8-flash` (Fast multimodal / scoring assistant)
  - `gemini-3.5-flash-lite` (High-speed classification)
  - `gemini-nano-banana-2.1` (8-pose character sheet generation / editing)
  - `gemini-3.5-transcribe` (Lyrics / speech transcription)
  - `lyria-3.5` (Music track generation)
  - `gemini-omni-1.1-flash` (Video generation / editing)
  - `antigravity-preview-09-2026` (Managed sandbox agent)
- **Argon Call Conventions**:
  - Use `thinking_level` (`low` / `medium` / `high`).
  - Do **NOT** pass deprecated/incompatible sampling args (`temperature`, `top_p`, `top_k`, `thinking_budget`, `cached_content`) when calling Argon.
  - For long multi-file generation, raise `max_output_tokens` and use generous HTTP timeouts or `background=True`.
  - Maintain a clean fallback model constant (`GEMINI_MODEL` from `.env`).

## 3. Verification Loop Requirements (Mandatory for Judging)
- **A. Musico (`musico/`)**:
  - Signal 1: Headless Playwright run with 0 console errors & >= 24 FPS average.
  - Signal 2: Deterministic clock `window.__seek(t)` / instrumentation hook verifying all Visual Score events fire within `±50ms` of planned timestamps.
  - Signal 3: Proxy frame/video inspection by Argon against the score's `why` checklist (with automatic code patch on failure).
- **B. YourDancer (`yourdancer/`)**:
  - Signal 1: Python Chart Validator (no same-lane notes within 80ms, NPS cap Easy<=2 / Normal<=4 / Hard<=7, no overlapping holds, all notes within duration).
  - Signal 2: Headless Playwright Auto-Player injecting exact note timings via deterministic hook to assert 100% Perfect accuracy and 0 console errors.
- **C. ReproFix (`reprofix/`)**:
  - Signal 1: Human-in-the-loop step approval before execution.
  - Signal 2: **Red-First Enforcement** — generated Playwright test MUST fail against the unpatched app (up to 3 re-scrubs if it accidentally passes).
  - Signal 3: Patch loop until new test + existing suite pass (Green), with GitHub credentials isolated from model context.

## 4. Environment & GCP Setup Notes (Verified)
- **gcloud CLI Path**: `/Users/uno/Downloads/google-cloud-sdk/bin/gcloud`
  - Always prepend `export PATH="/Users/uno/Downloads/google-cloud-sdk/bin:$PATH"` in shell commands.
- **ADC Credentials Path**: `/Users/uno/.config/gcloud/legacy_credentials/devstar2655@gcplab.me/adc.json`
  - Set `GOOGLE_APPLICATION_CREDENTIALS=/Users/uno/.config/gcloud/legacy_credentials/devstar2655@gcplab.me/adc.json` in `.env` so Python `google-cloud-*` libraries authenticate automatically.
- **GCP Project**: `h2gdm-hack26icn-2655` (`asia-northeast3`), Account: `devstar2655@gcplab.me`
- **Dual-Mode Storage**: Every service must work seamlessly with **local filesystem + JSON/SQLite state** AND sync to GCS/Firestore when configured.

## 5. Exact Interactions API Code Patterns (`google-genai >= 2.30.1`)

### Standard & Structured Output Call
```python
from google import genai
from pydantic import BaseModel

client = genai.Client() # reads GEMINI_API_KEY from environment

interaction = client.interactions.create(
    model="gemini-4-argon",
    input="...",
    generation_config={
        "thinking_level": "medium", # "low" | "medium" | "high"
        "max_output_tokens": 65536,
    },
    response_format={
        "type": "text",
        "mime_type": "application/json",
        "schema": MySchema.model_json_schema(),
    },
)
print(interaction.output_text)
```

### Long Decode (>64K tokens) with Background Execution
```python
import time

interaction = client.interactions.create(
    model="gemini-4-argon",
    input="...",
    background=True,
    generation_config={
        "max_output_tokens": 262144,
        "thinking_level": "high",
    },
)
while interaction.status in ("in_progress", "queued"):
    time.sleep(5)
    interaction = client.interactions.get(id=interaction.id)

text = "".join(
    content.text
    for step in interaction.steps
    if step.type == "model_output"
    for content in step.content
    if content.type == "text"
)
```

### Antigravity Managed Agent (`antigravity-preview-09-2026`)
```python
interaction = client.interactions.create(
    agent="antigravity-preview-09-2026",
    input="...",
    environment="remote",
    agent_config={
        "type": "antigravity",
        "model": "gemini-4-argon",
    },
)
print(interaction.environment_id, interaction.output_text)
```
