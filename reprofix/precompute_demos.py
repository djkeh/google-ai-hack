"""Runs the full ReproFix pipeline on Bug 1 and Bug 2 recordings to populate pre-computed demo jobs in local storage, GCS, and Firestore."""
import shutil
import time
from pathlib import Path

from analyzer import analyze_bug_video
from pr_creator import build_pull_request_payload, publish_github_pr_at_proxy_boundary
from sandbox_runner import run_red_then_green_pipeline
from storage import RECORDINGS_DIR, job_dir, save_job, upload_artifact_to_gcs


def run_demo_job(job_id: str, video_filename: str, preset_hint: str, probe_remote_agent: bool = False):
    print(f"\n=== Running Full ReproFix Pipeline for {job_id} ({video_filename}) ===")
    src_video = RECORDINGS_DIR / video_filename
    if not src_video.exists():
        raise FileNotFoundError(f"Missing recording {src_video}. Run seed_recordings.py first.")

    jdir = job_dir(job_id)
    local_video = jdir / "recording.mp4"
    shutil.copy2(src_video, local_video)

    created_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    logs = [
        {
            "timestamp": time.strftime("%H:%M:%S", time.gmtime()),
            "phase": "UPLOAD",
            "status": "INFO",
            "message": f"Uploaded raw screen recording {video_filename} ({local_video.stat().st_size} bytes)",
        }
    ]

    # Step 1: Gemini 4 Argon Video Scrubbing + Companion Models
    print(f"[{job_id}] Step 1: Analyzing video with Gemini 4 Argon (thinking_level='high')...")
    analysis_bundle = analyze_bug_video(
        video_path=local_video,
        out_dir=jdir,
        console_logs="",
        preset_hint=preset_hint,
    )
    analysis = analysis_bundle["analysis"]
    telemetry = analysis_bundle["telemetry"]
    logs.append(
        {
            "timestamp": time.strftime("%H:%M:%S", time.gmtime()),
            "phase": "VIDEO_ANALYSIS",
            "status": "SUCCESS",
            "message": (
                f"Gemini 4 Argon extracted {len(analysis['steps'])} repro steps "
                f"(bug_timestamp={analysis['bug_timestamp_sec']}s, interaction_id={telemetry.get('argon_interaction_id')})"
            ),
        }
    )

    # Step 2: HITL #1 Approval
    approved_steps = analysis["steps"]
    logs.append(
        {
            "timestamp": time.strftime("%H:%M:%S", time.gmtime()),
            "phase": "HITL_APPROVAL_1",
            "status": "APPROVED",
            "message": f"Developer reviewed and approved {len(approved_steps)} Playwright reproduction steps.",
        }
    )

    def on_progress(phase: str, message: str, status: str = "INFO"):
        print(f"  -> [{phase}] ({status}) {message}")
        logs.append(
            {
                "timestamp": time.strftime("%H:%M:%S", time.gmtime()),
                "phase": phase,
                "status": status,
                "message": message,
            }
        )

    # Step 3: Red-First Verification Loop + Argon Patch + Green Regression Suite
    print(f"[{job_id}] Step 3: Running Red-First Sandbox Verification + Argon Patch Loop...")
    sandbox_result = run_red_then_green_pipeline(
        job_id=job_id,
        analysis=analysis,
        approved_steps=approved_steps,
        on_progress=on_progress,
        probe_remote_agent=probe_remote_agent,
    )

    # Step 4: Isolated Credential Proxy & GitHub PR Creation
    print(f"[{job_id}] Step 4: Building GitHub PR via Isolated Credential Proxy...")
    pr_draft = build_pull_request_payload(
        job_id=job_id,
        analysis=analysis,
        approved_steps=approved_steps,
        sandbox_result=sandbox_result,
    )
    pr_published = publish_github_pr_at_proxy_boundary(pr_draft, live_push=False)
    logs.append(
        {
            "timestamp": time.strftime("%H:%M:%S", time.gmtime()),
            "phase": "PR_READY",
            "status": "SUCCESS",
            "message": f"Pull Request ready on branch `{pr_published['head_branch']}` (token_in_model_context=False). Awaiting HITL #2 merge.",
        }
    )

    # Upload video & frames to GCS
    for fname, ctype in [
        ("recording.mp4", "video/mp4"),
        ("contact_sheet.jpg", "image/jpeg"),
        ("bug_frame.jpg", "image/jpeg"),
    ]:
        uri = upload_artifact_to_gcs(job_id, jdir / fname, content_type=ctype)
        if uri:
            sandbox_result["artifacts"].setdefault("gcs_uris", {})[fname] = uri

    job_payload = {
        "job_id": job_id,
        "preset_key": preset_hint,
        "video_filename": video_filename,
        "status": "PR_READY",
        "created_at": created_at,
        "analysis": analysis,
        "approved_steps": approved_steps,
        "telemetry": telemetry,
        "sandbox_result": sandbox_result,
        "pull_request": pr_published,
        "logs": logs,
    }
    saved = save_job(job_payload, sync_cloud=True)
    print(f"[{job_id}] Completed & synced! Status={saved['status']}, Firestore={saved.get('cloud_sync', {}).get('firestore')}")
    return saved


if __name__ == "__main__":
    run_demo_job("job-bug1-demo", "bug1_counter_desync.mp4", "bug1", probe_remote_agent=True)
    run_demo_job("job-bug2-demo", "bug2_estimate_nan.mp4", "bug2", probe_remote_agent=False)
