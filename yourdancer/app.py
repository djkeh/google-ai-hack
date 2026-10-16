import logging
import shutil
import threading
import time
import uuid
from pathlib import Path
from typing import Any, Dict, Optional

import uvicorn
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from chart_builder import build_and_verify_charts
from config import (
    GCP_PROJECT_ID,
    GCS_BUCKET_NAME,
    GEMINI_FLASH_MODEL as FAST_MODEL,
    GEMINI_MODEL,
    JOBS_DIR,
    PORT,
    STATIC_DIR,
    VIDEOS_DIR,
)
from pipeline import ensure_precomputed_demo_jobs, run_yourdancer_pipeline
from seed_video import ensure_seed_videos
from storage import storage_manager
from verifier import verify_game_with_playwright

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("yourdancer.app")

app = FastAPI(
    title="YourDancer — AI Dance Video to 4-Lane Rhythm Game",
    description=(
        "Track 1: Multimodal Video Move Extraction (Gemini 4 Argon) + Librosa Audio Onset Snapping "
        "+ 3-Difficulty Chart Validator (Fail -> Patch -> Pass) + Headless Playwright Auto-Player."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount jobs directory so `/jobs/{job_id}/game/index.html` works as a standalone multi-file rhythm game
JOBS_DIR.mkdir(parents=True, exist_ok=True)
VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
STATIC_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/jobs", StaticFiles(directory=str(JOBS_DIR)), name="jobs")
app.mount("/videos", StaticFiles(directory=str(VIDEOS_DIR)), name="videos")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.on_event("startup")
def on_startup() -> None:
    """Ensure seed videos exist on startup; if demo jobs aren't created yet, start them in background."""
    try:
        ensure_seed_videos()
        existing = storage_manager.list_jobs()
        demo_ids = {j.get("job_id") for j in existing if j.get("status") == "completed"}
        if "demo_kpop_electro_groove" not in demo_ids or "demo_urban_street_choreo" not in demo_ids:
            logger.info("Precomputed demo jobs missing or incomplete; launching background warmup...")
            threading.Thread(target=ensure_precomputed_demo_jobs, kwargs={"force": False}, daemon=True).start()
    except Exception as exc:
        logger.warning("Startup check warning: %s", exc)


@app.get("/", response_class=HTMLResponse)
def read_index() -> FileResponse:
    index_path = STATIC_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="UI index.html not found")
    return FileResponse(index_path)


@app.get("/api/health")
def api_health() -> Dict[str, Any]:
    jobs = storage_manager.list_jobs()
    completed_jobs = [j for j in jobs if j.get("status") == "completed"]
    return {
        "status": "ok",
        "service": "yourdancer",
        "port": PORT,
        "gemini_model": GEMINI_MODEL,
        "fast_model": FAST_MODEL,
        "gcp_project": GCP_PROJECT_ID,
        "gcs_bucket": GCS_BUCKET_NAME,
        "total_jobs": len(jobs),
        "completed_jobs": len(completed_jobs),
    }


@app.get("/api/jobs")
def api_list_jobs() -> Dict[str, Any]:
    jobs = storage_manager.list_jobs()
    summaries = []
    for j in jobs:
        ver = j.get("verification", {})
        s1 = ver.get("signal_1_chart_validator", {})
        s2 = ver.get("signal_2_playwright_autoplayer", {})
        summaries.append(
            {
                "job_id": j.get("job_id"),
                "title": j.get("title"),
                "subtitle": j.get("subtitle"),
                "status": j.get("status"),
                "current_stage": j.get("current_stage"),
                "created_at": j.get("created_at"),
                "updated_at": j.get("updated_at"),
                "bpm": j.get("bpm"),
                "duration": j.get("duration"),
                "choreo_style": j.get("choreo_style"),
                "total_moves": len(j.get("snapped_moves", [])),
                "mean_snap_ms": j.get("snap_stats", {}).get("mean_snap_ms"),
                "chart_summary": j.get("chart_summary", {}),
                "signal_1_status": s1.get("status", "PENDING"),
                "signal_2_status": s2.get("status", "PENDING"),
                "overall_passed": ver.get("overall_passed", False),
                "game_url": j.get("game_url", f"/jobs/{j.get('job_id')}/game/index.html"),
                "preview_gameplay_url": j.get("preview_gameplay_url"),
                "preview_results_url": j.get("preview_results_url"),
                "firestore_synced": j.get("firestore_synced", False),
                "gcs": j.get("gcs", {}),
            }
        )
    return {"jobs": summaries}


@app.get("/api/jobs/{job_id}")
def api_get_job(job_id: str) -> Dict[str, Any]:
    job = storage_manager.load_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Job '{job_id}' not found")
    return job


@app.post("/api/jobs/{job_id}/reverify")
def api_reverify_job(job_id: str) -> Dict[str, Any]:
    """
    Fast Live Verification endpoint (< 4 seconds) for live hackathon judging:
    Re-runs Signal 1 (Python Chart Validator Fail -> Patch -> Pass loop) and
    Signal 2 (Headless Playwright Auto-Player 100% Perfect + 120ms Jitter Miss test)
    against the job's generated game bundle and updates local + Firestore state.
    """
    job = storage_manager.load_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Job '{job_id}' not found")

    t0 = time.time()
    snapped_moves = job.get("snapped_moves", [])
    duration = float(job.get("duration", 35.0))
    bpm = float(job.get("bpm", 120.0))

    # Re-run Signal 1 Validator (Fail -> Patch -> Pass)
    chart_bundle = build_and_verify_charts(
        snapped_moves=snapped_moves,
        duration=duration,
        bpm=bpm,
        call_argon_fixer=False,
    )
    signal_1 = chart_bundle["signal_1"]

    # Re-run Signal 2 Headless Playwright Auto-Player
    game_dir = storage_manager.job_dir(job_id) / "game"
    if not (game_dir / "index.html").exists():
        raise HTTPException(status_code=400, detail=f"Game bundle missing for job '{job_id}'")

    signal_2 = verify_game_with_playwright(game_dir)
    elapsed = round(time.time() - t0, 2)

    job["verification"] = {
        "overall_passed": signal_1["status"] == "PASS" and signal_2["status"] == "PASS",
        "last_live_verified_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "live_verification_elapsed_seconds": elapsed,
        "signal_1_chart_validator": signal_1,
        "signal_2_playwright_autoplayer": signal_2,
    }
    storage_manager.save_job(job_id, job, sync_cloud=True)
    return {
        "job_id": job_id,
        "elapsed_seconds": elapsed,
        "verification": job["verification"],
    }


@app.post("/api/jobs/upload")
async def api_upload_video(
    title: str = Form("Custom Dance Practice Routine"),
    subtitle: str = Form("Uploaded Dance Video · 4-Limb Extraction"),
    bpm_hint: float = Form(120.0),
    fast_mode: bool = Form(True),
    preset_key: Optional[str] = Form(None),
    video: Optional[UploadFile] = File(None),
) -> Dict[str, Any]:
    """
    Starts a new YourDancer pipeline job from either an uploaded MP4 video or a preset camera routine.
    """
    job_id = f"custom_{uuid.uuid4().hex[:8]}"
    job_dir = storage_manager.job_dir(job_id)
    seed_spec = None

    if video is not None and video.filename:
        safe_name = Path(video.filename).name
        if not safe_name.lower().endswith((".mp4", ".mov", ".webm")):
            safe_name += ".mp4"
        video_path = job_dir / safe_name
        with open(video_path, "wb") as f:
            shutil.copyfileobj(video.file, f)
    else:
        specs = ensure_seed_videos()
        chosen_key = preset_key if (preset_key and preset_key in specs) else "kpop_electro_groove"
        seed_spec = specs[chosen_key]
        video_path = Path(seed_spec["mp4_path"])
        bpm_hint = float(seed_spec["bpm"])
        if title == "Custom Dance Practice Routine":
            title = f"{seed_spec['title']} (Live Run)"

    initial_job = {
        "job_id": job_id,
        "title": title,
        "subtitle": subtitle,
        "status": "running",
        "current_stage": "1_extracting_moves",
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    storage_manager.save_job(job_id, initial_job, sync_cloud=False)

    def _bg() -> None:
        try:
            run_yourdancer_pipeline(
                job_id=job_id,
                video_path=video_path,
                title=title,
                subtitle=subtitle,
                fallback_bpm=bpm_hint,
                seed_spec=seed_spec,
                use_fast_model=fast_mode,
                sync_cloud=True,
            )
        except Exception as exc:
            logger.exception("Pipeline failed for job %s: %s", job_id, exc)
            err_job = storage_manager.load_job(job_id) or initial_job
            err_job["status"] = "failed"
            err_job["error"] = str(exc)
            storage_manager.save_job(job_id, err_job, sync_cloud=False)

    threading.Thread(target=_bg, daemon=True).start()
    return {"job_id": job_id, "status": "running", "title": title}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=PORT, reload=False)
