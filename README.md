# 2026 Google AI Hackathon — Gemini 4 Argon Projects

Built in a 4-hour sprint using **Gemini 4 Argon (`gemini-4-argon`)** via the Google GenAI Interactions API (`google-genai >= 2.30.1`), **Cloud Run**, **Cloud Storage**, and **Cloud Firestore**.

## Projects in This Repository

| Project | Track | Directory | Description |
| :--- | :--- | :--- | :--- |
| **A. Musico** *(formerly Choreograph)* | Track 1 (Entertainment) | [`musico/`](./musico/) | **AI Motion-Graphics Director**: Listens to a full track + `librosa` onset features, authors a timed `Visual Score` with explicit directorial reasoning (`why`), generates a multi-file 2D Sprite/Canvas animation scene, and self-verifies via headless Playwright (`±50ms` deterministic clock check + Argon visual proxy inspection). |
| **B. YourDancer** *(formerly MoveChart)* | Track 1 (Entertainment) | [`yourdancer/`](./yourdancer/) | **Dance Video to Playable 4-Lane Rhythm Game**: Scrubs a dance video with Gemini 4 Argon to extract limb move units (`L_arm`, `R_arm`, `L_leg`, `R_leg`), snaps impact frames to `librosa` audio onsets for `±50ms` accuracy, builds Easy/Normal/Hard charts, generates a 4-lane rhythm game, and verifies 100% playability with a Python chart validator + headless Playwright auto-player. |
| **C. ReproFix** | Track 4 (Autonomous Agents & DevTools) | [`reprofix/`](./reprofix/) | **Raw Bug Recording to Red-then-Green Pull Request**: Watches an uninstrumented screen recording of a web app bug, extracts timestamped reproduction steps (with Human-in-the-Loop approval), enforces a **Red-First** Playwright test check (must fail before patching), patches the code until Green, and opens a GitHub PR with isolated credentials. |

## Quick Setup

```bash
cp .env.example .env
# Populate GEMINI_API_KEY and GCP_PROJECT_ID in .env

python3 -m venv .venv
.venv/bin/pip install -U "google-genai>=2.30.1" fastapi "uvicorn[standard]" python-multipart pydantic python-dotenv librosa soundfile numpy scipy pillow playwright google-cloud-storage google-cloud-firestore httpx pytest
.venv/bin/playwright install chromium
```

## License

MIT License — see [LICENSE](./LICENSE).
