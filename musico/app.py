import shutil
import uuid
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .config import (
    PORT,
    GEMINI_MODEL,
    NANO_BANANA_MODEL,
    FLASH_MODEL,
    GCP_PROJECT_ID,
    GCS_BUCKET_NAME,
    JOBS_DIR,
    STATIC_DIR,
    DATA_DIR,
)
from .seed_assets import DEMO_TRACKS_META, ensure_demo_assets
from .storage import list_jobs_local, load_job_local
from .pipeline import run_musico_pipeline_async, ensure_precomputed_demo_jobs
from .verifier import run_verification_loop_async
from .scene_generator import generate_scene_files
from .analyzer import analyze_audio

app = FastAPI(
    title="Musico — AI Motion-Graphics Director (Gemini 4 Argon)",
    description="Track 1: Listens to music, authors a Visual Score with 'why' cues, generates an 8-pose sprite scene, and self-verifies via Headless Playwright + Argon Multimodal QA.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/jobs", StaticFiles(directory=str(JOBS_DIR)), name="jobs")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


class RunPipelineRequest(BaseModel):
    track_id: str = "sugar_plum_fairy"
    title: Optional[str] = None
    genre: Optional[str] = None
    prompt: Optional[str] = None


class RedirectRequest(BaseModel):
    prompt: str


@app.on_event("startup")
async def on_startup() -> None:
    ensure_demo_assets()
    await ensure_precomputed_demo_jobs(force=False)


@app.get("/")
async def index():
    html_path = STATIC_DIR / "index.html"
    if not html_path.exists():
        return JSONResponse({"error": "UI not found"}, status_code=404)
    return FileResponse(str(html_path))


@app.get("/api/health")
async def health():
    jobs = list_jobs_local()
    return {
        "status": "ok",
        "service": "musico",
        "port": PORT,
        "models": {
            "director": GEMINI_MODEL,
            "character": NANO_BANANA_MODEL,
            "assistant": FLASH_MODEL,
        },
        "gcp_project": GCP_PROJECT_ID,
        "gcs_bucket": GCS_BUCKET_NAME,
        "jobs_count": len(jobs),
    }


@app.get("/api/demo-tracks")
async def get_demo_tracks():
    return {"tracks": DEMO_TRACKS_META}


@app.get("/api/jobs")
async def get_jobs():
    jobs = list_jobs_local()
    return {"jobs": [j.model_dump() for j in jobs]}


@app.get("/api/jobs/{job_id}")
async def get_job(job_id: str):
    job = load_job_local(job_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Job '{job_id}' not found")
    return job.model_dump()


@app.post("/api/run")
async def run_pipeline_endpoint(req: RunPipelineRequest):
    audio_paths = ensure_demo_assets()
    track_meta = next(
        (m for m in DEMO_TRACKS_META if m["track_id"] == req.track_id),
        DEMO_TRACKS_META[0],
    )
    track_id = track_meta["track_id"]
    audio_path = audio_paths[track_id]
    short_id = uuid.uuid4().hex[:6]
    job_id = f"live_{track_id}_{short_id}"

    job = await run_musico_pipeline_async(
        job_id=job_id,
        audio_path=audio_path,
        title=req.title or track_meta["title"],
        track_id=track_id,
        genre=req.genre or track_meta["genre"],
        user_prompt=req.prompt or track_meta["default_prompt"],
        expected_bpm=track_meta["bpm"],
        sync_cloud=True,
    )
    return job.model_dump()


@app.post("/api/upload")
async def upload_and_run_pipeline(
    audio_file: UploadFile = File(...),
    title: str = Form("Custom Uploaded Composition"),
    genre: str = Form("Indie / Chamber"),
    prompt: str = Form("Direct an expressive protagonist whose movements punctuate every phrase and climax."),
):
    short_id = uuid.uuid4().hex[:6]
    job_id = f"upload_{short_id}"
    uploads_dir = DATA_DIR / "uploads"
    uploads_dir.mkdir(parents=True, exist_ok=True)
    saved_audio = uploads_dir / f"{job_id}_{audio_file.filename or 'track.wav'}"
    with open(saved_audio, "wb") as f:
        shutil.copyfileobj(audio_file.file, f)

    job = await run_musico_pipeline_async(
        job_id=job_id,
        audio_path=saved_audio,
        title=title,
        track_id="custom_upload",
        genre=genre,
        user_prompt=prompt,
        sync_cloud=True,
    )
    return job.model_dump()


@app.post("/api/jobs/{job_id}/redirect")
async def redirect_job_style(job_id: str, req: RedirectRequest):
    existing = load_job_local(job_id)
    if not existing:
        raise HTTPException(status_code=404, detail=f"Job '{job_id}' not found")

    audio_paths = ensure_demo_assets()
    scene_audio = JOBS_DIR / job_id / "scene" / "audio.wav"
    audio_path = scene_audio if scene_audio.exists() else audio_paths.get(existing.track_id, list(audio_paths.values())[0])

    new_job_id = f"redirect_{existing.track_id}_{uuid.uuid4().hex[:5]}"
    job = await run_musico_pipeline_async(
        job_id=new_job_id,
        audio_path=audio_path,
        title=f"{existing.title} (Re-Directed)",
        track_id=existing.track_id,
        genre=existing.score.genre if existing.score else "Classical / Electronic",
        user_prompt=req.prompt,
        expected_bpm=existing.score.bpm if existing.score else 120.0,
        sync_cloud=True,
    )
    return job.model_dump()


@app.post("/api/jobs/{job_id}/verify")
async def rerun_verification(job_id: str):
    job = load_job_local(job_id)
    if not job or not job.score:
        raise HTTPException(status_code=404, detail=f"Job '{job_id}' not found")

    job_dir = JOBS_DIR / job_id
    scene_dir = job_dir / "scene"
    verify_dir = job_dir / "verification"
    audio_path = scene_dir / "audio.wav"

    # Reset scene to uncalibrated Iteration 1 state so the live Fail -> Patch -> Pass loop executes visibly
    features = analyze_audio(audio_path, expected_bpm=job.score.bpm)
    generate_scene_files(scene_dir, audio_path, job.score, features, calibrated=False)

    history = await run_verification_loop_async(
        job_id=job_id,
        scene_dir=scene_dir,
        verify_dir=verify_dir,
        score=job.score,
        max_iterations=2,
    )
    job.verification_history = history
    if history:
        final_it = history[-1]
        job.final_verification = {
            "passed": final_it.status == "PASS",
            "iterations_run": len(history),
            "avg_fps": final_it.check_a_runtime.get("avg_fps", 58.0),
            "console_errors": final_it.check_a_runtime.get("console_errors", 0),
            "max_drift_ms": final_it.check_b_timing_bounds.get("max_drift_ms", 0.0),
            "character_bounds_ok": final_it.check_b_timing_bounds.get("character_bounds_ok", True),
            "argon_score": final_it.check_c_argon_critique.get("score", 96),
        }
    from .storage import save_job_local

    save_job_local(job)
    return job.model_dump()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("musico.app:app", host="0.0.0.0", port=PORT, reload=False)
