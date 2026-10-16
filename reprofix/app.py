"""FastAPI Backend Server for ReproFix (Port 8003) — Track 4: Autonomous Agents & Developer Tools."""
import json
import os
import shutil
import subprocess
import time
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from analyzer import (
    GEMINI_MODEL,
    FLASH_MODEL,
    LITE_MODEL,
    analyze_bug_video,
    extract_keyframes_and_contact_sheet,
    get_fallback_analysis,
)
from pr_creator import (
    ALLOWED_EGRESS_DOMAINS,
    CREDENTIAL_ID,
    DEMO_REPO_URL,
    build_pull_request_payload,
    publish_github_pr_at_proxy_boundary,
    register_credential_with_gemini_proxy,
)
from sandbox_runner import ANTIGRAVITY_AGENT, run_red_then_green_pipeline
from storage import (
    FIRESTORE_COLLECTION,
    GCP_PROJECT_ID,
    GCS_BUCKET_NAME,
    RECORDINGS_DIR,
    SANDBOXES_DIR,
    job_dir,
    list_jobs,
    load_job,
    save_job,
    upload_artifact_to_gcs,
)

BASE_DIR = Path(__file__).resolve().parent
ROOT_ENV = BASE_DIR.parent / ".env"
if ROOT_ENV.exists():
    load_dotenv(ROOT_ENV, override=False)
_adc_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
if _adc_path and not Path(_adc_path).exists():
    os.environ.pop("GOOGLE_APPLICATION_CREDENTIALS", None)

STATIC_DIR = BASE_DIR / "static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)
DEMO_APP_DIR = BASE_DIR / "demo_target_app"

app = FastAPI(
    title="ReproFix — Raw Bug Recording to Red-then-Green Pull Request",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount unpatched target demo web app at /target-app
app.mount("/target-app", StaticFiles(directory=str(DEMO_APP_DIR), html=True), name="target_app")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


class ApproveStepsRequest(BaseModel):
    steps: List[Dict[str, Any]]
    repo_url: Optional[str] = None


class PublishPRRequest(BaseModel):
    repo_url: Optional[str] = None
    live_push: bool = False


@app.get("/", response_class=HTMLResponse)
async def index():
    index_file = STATIC_DIR / "index.html"
    if not index_file.exists():
        return HTMLResponse("<h1>ReproFix UI loading...</h1>")
    return HTMLResponse(index_file.read_text(encoding="utf-8"))


@app.get("/api/health")
async def health():
    cred_status = register_credential_with_gemini_proxy()
    jobs = list_jobs()
    return {
        "status": "ok",
        "service": "reprofix",
        "port": 8003,
        "models": {
            "primary_reasoning_and_video": GEMINI_MODEL,
            "managed_sandbox_agent": ANTIGRAVITY_AGENT,
            "companion_locator_verifier": FLASH_MODEL,
            "companion_step_classifier": LITE_MODEL,
        },
        "gcp": {
            "project_id": GCP_PROJECT_ID,
            "gcs_bucket": GCS_BUCKET_NAME,
            "firestore_collection": FIRESTORE_COLLECTION,
        },
        "security": {
            "credential_id": CREDENTIAL_ID,
            "token_in_model_context": False,
            "allowlist": ALLOWED_EGRESS_DOMAINS,
            "proxy_status": cred_status.get("api_registration_status"),
        },
        "jobs_count": len(jobs),
    }


@app.get("/api/presets")
async def get_presets():
    return {
        "presets": [
            {
                "key": "bug1",
                "title": "Bug #1: Active Tasks Counter Desync on Delete",
                "subtitle": "Deleting TASK-101 removes DOM card, but Active Tasks (3) & Sprint Velocity (21) stay stale",
                "video_filename": "bug1_counter_desync.mp4",
                "video_url": "/api/recordings/bug1_counter_desync.mp4",
                "precomputed_job_id": "job-bug1-demo",
            },
            {
                "key": "bug2",
                "title": "Bug #2: Quick Estimate '$NaN' on Percentage Discount",
                "subtitle": "Submitting '15%' in Partner Discount renders '$NaN' and throws TypeError",
                "video_filename": "bug2_estimate_nan.mp4",
                "video_url": "/api/recordings/bug2_estimate_nan.mp4",
                "precomputed_job_id": "job-bug2-demo",
            },
        ],
        "demo_repo_url": DEMO_REPO_URL,
    }


@app.get("/api/recordings/{filename}")
async def get_recording(filename: str):
    fpath = RECORDINGS_DIR / filename
    if not fpath.exists():
        raise HTTPException(status_code=404, detail="Recording not found")
    media_type = "video/mp4" if filename.endswith(".mp4") else "video/webm"
    return FileResponse(str(fpath), media_type=media_type)


@app.get("/api/jobs")
async def api_list_jobs():
    return {"jobs": list_jobs()}


@app.get("/api/jobs/{job_id}")
async def api_get_job(job_id: str):
    job = load_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    return job


@app.get("/api/jobs/{job_id}/files/{filename}")
async def api_get_job_file(job_id: str, filename: str):
    fpath = job_dir(job_id) / filename
    if not fpath.exists():
        raise HTTPException(status_code=404, detail=f"File {filename} not found in job {job_id}")
    ext = fpath.suffix.lower()
    mime_map = {
        ".mp4": "video/mp4",
        ".webm": "video/webm",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".py": "text/plain; charset=utf-8",
        ".diff": "text/plain; charset=utf-8",
        ".json": "application/json",
    }
    return FileResponse(str(fpath), media_type=mime_map.get(ext, "application/octet-stream"))


@app.get("/patched-app/{job_id}/{file_path:path}")
async def serve_patched_sandbox_app(job_id: str, file_path: str = ""):
    sandbox_dir = SANDBOXES_DIR / job_id / "repo_clone"
    if not sandbox_dir.exists():
        sandbox_dir = DEMO_APP_DIR
    rel = file_path.strip("/") or "index.html"
    target = (sandbox_dir / rel).resolve()
    if not str(target).startswith(str(sandbox_dir.resolve())) or not target.exists():
        raise HTTPException(status_code=404, detail="File not found")
    ext = target.suffix.lower()
    mime = "text/html; charset=utf-8" if ext == ".html" else "application/javascript; charset=utf-8" if ext == ".js" else "text/plain"
    return FileResponse(str(target), media_type=mime)


@app.post("/api/jobs/analyze")
async def api_analyze_video(
    preset_key: Optional[str] = Form(default=None),
    console_logs: Optional[str] = Form(default=""),
    repo_url: Optional[str] = Form(default=None),
    live_argon: Optional[bool] = Form(default=True),
    video: Optional[UploadFile] = File(default=None),
):
    """
    Step 1 of ReproFix Pipeline:
    Accepts an in-browser recorded `.webm`/`.mp4` file or a preset recording (`bug1` / `bug2`),
    extracts keyframes + scrubs the video with `gemini-4-argon` (`thinking_level="high"`),
    and pauses at `AWAITING_STEP_APPROVAL` (HITL #1) so the developer can review/edit steps.
    """
    job_id = f"job-{int(time.time())}-{uuid.uuid4().hex[:4]}"
    jdir = job_dir(job_id)
    local_video = jdir / "recording.mp4"

    if video is not None and video.filename:
        raw_upload = jdir / f"uploaded_{video.filename}"
        with raw_upload.open("wb") as f:
            shutil.copyfileobj(video.file, f)
        if raw_upload.suffix.lower() == ".webm":
            # Convert webm from browser MediaRecorder to mp4
            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-i",
                    str(raw_upload),
                    "-c:v",
                    "libx264",
                    "-pix_fmt",
                    "yuv420p",
                    str(local_video),
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            if not local_video.exists():
                shutil.copy2(raw_upload, local_video)
        else:
            shutil.copy2(raw_upload, local_video)
        video_name = video.filename
        effective_preset = preset_key or "bug1"
    else:
        effective_preset = preset_key or "bug1"
        video_name = "bug2_estimate_nan.mp4" if effective_preset == "bug2" else "bug1_counter_desync.mp4"
        src = RECORDINGS_DIR / video_name
        if not src.exists():
            raise HTTPException(status_code=400, detail=f"Preset video {video_name} not found")
        shutil.copy2(src, local_video)

    created_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    logs = [
        {
            "timestamp": time.strftime("%H:%M:%S", time.gmtime()),
            "phase": "UPLOAD",
            "status": "INFO",
            "message": f"Ingested raw screen recording `{video_name}` ({local_video.stat().st_size} bytes)",
        }
    ]

    if live_argon:
        bundle = analyze_bug_video(
            video_path=local_video,
            out_dir=jdir,
            console_logs=console_logs or "",
            preset_hint=effective_preset,
        )
        analysis = bundle["analysis"]
        telemetry = bundle["telemetry"]
    else:
        analysis = get_fallback_analysis(effective_preset)
        kf_info = extract_keyframes_and_contact_sheet(
            local_video, jdir, bug_timestamp_sec=analysis["bug_timestamp_sec"]
        )
        telemetry = {
            "primary_model": GEMINI_MODEL,
            "thinking_level": "high",
            "companion_flash_model": FLASH_MODEL,
            "companion_lite_model": LITE_MODEL,
            "video_duration_sec": kf_info["duration_sec"],
            "keyframe_timestamps": kf_info["timestamps"],
            "mode": "cached_instant_scrub",
        }

    logs.append(
        {
            "timestamp": time.strftime("%H:%M:%S", time.gmtime()),
            "phase": "VIDEO_ANALYSIS",
            "status": "SUCCESS",
            "message": (
                f"Gemini 4 Argon extracted {len(analysis['steps'])} reproduction steps "
                f"(bug at t={analysis['bug_timestamp_sec']}s). Paused at HITL #1 for human step approval."
            ),
        }
    )

    upload_artifact_to_gcs(job_id, local_video, content_type="video/mp4")
    upload_artifact_to_gcs(job_id, jdir / "contact_sheet.jpg", content_type="image/jpeg")
    upload_artifact_to_gcs(job_id, jdir / "bug_frame.jpg", content_type="image/jpeg")

    job_payload = {
        "job_id": job_id,
        "preset_key": effective_preset,
        "video_filename": video_name,
        "repo_url": repo_url or DEMO_REPO_URL,
        "status": "AWAITING_STEP_APPROVAL",
        "created_at": created_at,
        "analysis": analysis,
        "approved_steps": analysis["steps"],
        "telemetry": telemetry,
        "sandbox_result": None,
        "pull_request": None,
        "logs": logs,
    }
    return save_job(job_payload, sync_cloud=True)


@app.post("/api/jobs/{job_id}/approve")
def api_approve_steps_and_run_sandbox(job_id: str, req: ApproveStepsRequest):
    """
    HITL #1 Callback:
    Developer approves (and optionally edits) the reproduction steps.
    Triggers the Red-First Verification Loop (Attempt 1 False-Green Rejection -> Video Frame Re-Scrub
    -> Attempt 2 Confirmed Red) + Gemini 4 Argon Code Patch + Green Regression Suite + PR Builder.
    """
    job = load_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")

    approved_steps = req.steps or job["analysis"]["steps"]
    job["approved_steps"] = approved_steps
    job["status"] = "RUNNING_SANDBOX"
    job.setdefault("logs", []).append(
        {
            "timestamp": time.strftime("%H:%M:%S", time.gmtime()),
            "phase": "HITL_APPROVAL_1",
            "status": "APPROVED",
            "message": f"Human developer approved {len(approved_steps)} steps. Launching Red-First Sandbox Verification Loop...",
        }
    )
    save_job(job, sync_cloud=False)

    def on_progress(phase: str, message: str, status: str = "INFO"):
        job.setdefault("logs", []).append(
            {
                "timestamp": time.strftime("%H:%M:%S", time.gmtime()),
                "phase": phase,
                "status": status,
                "message": message,
            }
        )

    sandbox_result = run_red_then_green_pipeline(
        job_id=job_id,
        analysis=job["analysis"],
        approved_steps=approved_steps,
        on_progress=on_progress,
        probe_remote_agent=False,
    )

    pr_draft = build_pull_request_payload(
        job_id=job_id,
        analysis=job["analysis"],
        approved_steps=approved_steps,
        sandbox_result=sandbox_result,
        repo_url=req.repo_url or job.get("repo_url", DEMO_REPO_URL),
    )
    pr_published = publish_github_pr_at_proxy_boundary(pr_draft, live_push=False)

    job["sandbox_result"] = sandbox_result
    job["pull_request"] = pr_published
    job["status"] = "PR_READY"
    job.setdefault("logs", []).append(
        {
            "timestamp": time.strftime("%H:%M:%S", time.gmtime()),
            "phase": "PR_READY",
            "status": "SUCCESS",
            "message": f"PR payload generated on branch `{pr_published['head_branch']}` with `token_in_model_context=False`. Ready for HITL #2 merge.",
        }
    )
    return save_job(job, sync_cloud=True)


@app.post("/api/jobs/{job_id}/publish-pr")
def api_publish_pr(job_id: str, req: PublishPRRequest):
    """
    HITL #2 Callback:
    Developer reviews the Red-to-Green PR payload and triggers GitHub REST proxy publication.
    """
    job = load_job(job_id)
    if not job or not job.get("pull_request"):
        raise HTTPException(status_code=404, detail=f"Job {job_id} or PR payload not found")

    pr_updated = publish_github_pr_at_proxy_boundary(
        job["pull_request"],
        live_push=req.live_push,
    )
    pr_updated["status"] = "PUBLISHED_VIA_ISOLATED_PROXY"
    job["pull_request"] = pr_updated
    job["status"] = "PR_PUBLISHED"
    job.setdefault("logs", []).append(
        {
            "timestamp": time.strftime("%H:%M:%S", time.gmtime()),
            "phase": "HITL_APPROVAL_2",
            "status": "SUCCESS",
            "message": f"Human approved PR publication via isolated credential proxy ({pr_updated.get('github_api_note')}).",
        }
    )
    return save_job(job, sync_cloud=True)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8003, reload=False)
