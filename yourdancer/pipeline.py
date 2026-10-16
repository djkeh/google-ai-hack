import logging
import time
from pathlib import Path
from typing import Any, Dict, Optional

from chart_builder import build_and_verify_charts
from extractor import extract_moves_with_argon
from game_generator import generate_rhythm_game_bundle
from seed_video import ensure_seed_videos
from snapper import snap_moves_to_audio_onsets
from storage import storage_manager
from verifier import verify_game_with_playwright

logger = logging.getLogger("yourdancer.pipeline")


def run_yourdancer_pipeline(
    job_id: str,
    video_path: Path,
    title: str,
    subtitle: str = "Custom Dance Practice Video",
    fallback_bpm: float = 120.0,
    seed_spec: Optional[Dict[str, Any]] = None,
    use_fast_model: bool = False,
    sync_cloud: bool = True,
) -> Dict[str, Any]:
    """
    Executes the complete YourDancer pipeline for a dance practice video:
      Step 1: Gemini 4 Argon Video Scrubbing & Limb Move Extraction (Files API + Interactions API)
      Step 2: Librosa Audio Onset & Beat Grid Snapping (raw_t -> snapped_t precision lock)
      Step 3: 3-Difficulty 4-Lane Chart Compilation + Signal 1 Validator Loop (Fail -> Patch -> Pass)
      Step 4: Multi-File HTML5 Canvas Rhythm Game Generation (index.html, game.js, judge.js, chart.json, video.mp4)
      Step 5: Signal 2 Headless Playwright Auto-Player Verification (100% Perfect + 120ms Jitter Miss test)
      Step 6: Dual Storage Persistence (Local + Firestore `yourdancer_jobs` + GCS `gs://.../yourdancer/<job_id>/`)
    """
    t_start = time.time()
    job_dir = storage_manager.job_dir(job_id)

    job_data: Dict[str, Any] = {
        "job_id": job_id,
        "title": title,
        "subtitle": subtitle,
        "status": "running",
        "current_stage": "1_extracting_moves",
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "video_filename": video_path.name,
        "stages": [],
    }
    storage_manager.save_job(job_id, job_data, sync_cloud=False)

    # Stage 1: Gemini 4 Argon Move Extraction
    logger.info("[%s] Stage 1: Extracting limb moves with Gemini 4 Argon...", job_id)
    extraction = extract_moves_with_argon(
        video_path=video_path,
        seed_spec=seed_spec,
        use_fast_model=use_fast_model,
    )
    job_data["stages"].append(
        {
            "stage": "1_argon_video_extraction",
            "title": "Gemini 4 Argon Video Scrubbing & Limb Move Extraction",
            "status": "COMPLETED",
            "model": extraction["model"],
            "thinking_level": extraction["thinking_level"],
            "interaction_id": extraction["interaction_id"],
            "gemini_file_uri": extraction["gemini_file_uri"],
            "moves_extracted": len(extraction["moves"]),
            "elapsed_seconds": extraction["elapsed_seconds"],
        }
    )

    # Stage 2: Librosa Audio Onset Snapping
    logger.info("[%s] Stage 2: Snapping move timestamps to Librosa audio onsets...", job_id)
    job_data["current_stage"] = "2_onset_snapping"
    audio_source = Path(seed_spec["wav_path"]) if (seed_spec and seed_spec.get("wav_path")) else video_path
    snap_result = snap_moves_to_audio_onsets(
        audio_or_video_path=audio_source,
        extracted_moves=extraction["moves"],
        fallback_bpm=fallback_bpm,
    )
    snap_stats = snap_result["stats"]
    job_data["stages"].append(
        {
            "stage": "2_librosa_onset_snap",
            "title": "Librosa Audio Onset & Beat Grid Snapping",
            "status": "COMPLETED",
            "detected_bpm": snap_stats["detected_bpm"],
            "detected_onsets": snap_stats["detected_onset_count"],
            "mean_snap_ms": snap_stats["mean_snap_ms"],
            "max_snap_ms": snap_stats["max_snap_ms"],
            "p95_snap_ms": snap_stats["p95_snap_ms"],
        }
    )

    # Stage 3: 3-Difficulty Chart Builder + Signal 1 Validator (Fail -> Patch -> Pass)
    logger.info("[%s] Stage 3: Building 3-difficulty charts & running Signal 1 Validator loop...", job_id)
    job_data["current_stage"] = "3_chart_validation_loop"
    duration = float(snap_stats["duration_sec"])
    bpm = float(snap_stats["reference_bpm"])
    chart_bundle = build_and_verify_charts(
        snapped_moves=snap_result["moves"],
        duration=duration,
        bpm=bpm,
        call_argon_fixer=True,
    )
    signal_1 = chart_bundle["signal_1"]
    job_data["stages"].append(
        {
            "stage": "3_chart_validator_loop",
            "title": "Signal 1: Python Chart Playability Validator (Fail -> Patch -> Pass)",
            "status": signal_1["status"],
            "iterations_run": signal_1["iterations_run"],
            "iter1_violations": signal_1["history"][0]["total_violations"],
            "iter2_violations": signal_1["history"][1]["total_violations"],
        }
    )

    # Stage 4: Multi-File HTML5 Canvas 2D Rhythm Game Generation
    logger.info("[%s] Stage 4: Generating multi-file HTML5 Canvas 4-lane rhythm game...", job_id)
    job_data["current_stage"] = "4_generating_game"
    chart_payload = {
        "job_id": job_id,
        "title": title,
        "subtitle": subtitle,
        "choreo_style": extraction["choreo_style"],
        "dancer_coaching_notes": extraction["dancer_coaching_notes"],
        "bpm": bpm,
        "duration": duration,
        "sections": extraction["sections"],
        "snap_stats": snap_stats,
        "snapped_moves": snap_result["moves"],
        "difficulties": chart_bundle["charts"],
    }
    game_info = generate_rhythm_game_bundle(
        job_dir=job_dir,
        video_path=video_path,
        chart_payload=chart_payload,
    )
    job_data["stages"].append(
        {
            "stage": "4_multi_file_game_gen",
            "title": "Multi-File Canvas 2D Rhythm Game Generation",
            "status": "COMPLETED",
            "files": game_info["files"],
        }
    )

    # Stage 5: Signal 2 Headless Playwright Auto-Player Verification
    logger.info("[%s] Stage 5: Running Signal 2 Headless Playwright Auto-Player verification...", job_id)
    job_data["current_stage"] = "5_playwright_auto_player"
    signal_2 = verify_game_with_playwright(Path(game_info["game_dir"]))
    job_data["stages"].append(
        {
            "stage": "5_playwright_auto_player",
            "title": "Signal 2: Headless Playwright Auto-Player (100% Perfect + Jitter Test)",
            "status": signal_2["status"],
            "perfect_accuracy": signal_2["perfect_runs"]["Normal"]["accuracy"],
            "jitter_120ms_accuracy": signal_2["jitter_120ms_run"]["accuracy"],
            "console_errors": signal_2["console_error_count"],
        }
    )

    # Stage 6: Cloud Sync (GCS + Firestore)
    gcs_sync = {"gcs_synced": False, "gcs_prefix": f"gs://h2gdm-hack26icn-2655-assets/yourdancer/{job_id}/game"}
    if sync_cloud:
        logger.info("[%s] Stage 6: Syncing game bundle & charts to GCS and Firestore...", job_id)
        gcs_sync = storage_manager.sync_directory_to_gcs(job_id, Path(game_info["game_dir"]), prefix_subpath="game")

    job_data.update(
        {
            "status": "completed" if (signal_1["status"] == "PASS" and signal_2["status"] == "PASS") else "failed",
            "current_stage": "completed",
            "total_elapsed_seconds": round(time.time() - t_start, 2),
            "bpm": bpm,
            "duration": duration,
            "choreo_style": extraction["choreo_style"],
            "dancer_coaching_notes": extraction["dancer_coaching_notes"],
            "argon_extraction": {
                "model": extraction["model"],
                "thinking_level": extraction["thinking_level"],
                "interaction_id": extraction["interaction_id"],
                "gemini_file_uri": extraction["gemini_file_uri"],
                "total_moves": len(extraction["moves"]),
            },
            "sections": extraction["sections"],
            "snap_stats": snap_stats,
            "snapped_moves": snap_result["moves"],
            "chart_summary": {
                diff: {
                    "note_count": len(chart_bundle["charts"][diff]),
                    "hold_count": sum(1 for n in chart_bundle["charts"][diff] if n.get("type") == "hold"),
                    "peak_nps": signal_1["history"][1]["difficulties"][diff]["peak_nps"],
                    "nps_cap": signal_1["history"][1]["difficulties"][diff]["nps_cap"],
                }
                for diff in ("Easy", "Normal", "Hard")
            },
            "verification": {
                "overall_passed": signal_1["status"] == "PASS" and signal_2["status"] == "PASS",
                "signal_1_chart_validator": signal_1,
                "signal_2_playwright_autoplayer": signal_2,
            },
            "game_url": f"/jobs/{job_id}/game/index.html",
            "preview_gameplay_url": f"/jobs/{job_id}/game/preview_gameplay.png",
            "preview_results_url": f"/jobs/{job_id}/game/preview_results.png",
            "gcs": {
                "gcs_synced": gcs_sync.get("gcs_synced", False),
                "gcs_prefix": gcs_sync.get("gcs_prefix", ""),
                "uploaded_count": len(gcs_sync.get("uploaded_files", [])),
            },
        }
    )

    storage_manager.save_job(job_id, job_data, sync_cloud=sync_cloud)
    logger.info(
        "[%s] Pipeline complete in %.1fs (Signal 1=%s, Signal 2=%s, Firestore=%s, GCS=%s)",
        job_id,
        job_data["total_elapsed_seconds"],
        signal_1["status"],
        signal_2["status"],
        job_data.get("firestore_synced", False),
        job_data["gcs"]["gcs_synced"],
    )
    return job_data


def ensure_precomputed_demo_jobs(force: bool = False) -> Dict[str, Dict[str, Any]]:
    """Pre-computes both demo dance practice videos so the live demo has instant verified results."""
    specs = ensure_seed_videos()
    results: Dict[str, Dict[str, Any]] = {}
    for key, spec in specs.items():
        job_id = f"demo_{key}"
        existing = storage_manager.load_job(job_id)
        game_index = storage_manager.job_dir(job_id) / "game" / "index.html"
        if not force and existing and existing.get("status") == "completed" and game_index.exists():
            results[job_id] = existing
            continue
        results[job_id] = run_yourdancer_pipeline(
            job_id=job_id,
            video_path=Path(spec["mp4_path"]),
            title=spec["title"],
            subtitle=spec["subtitle"],
            fallback_bpm=float(spec["bpm"]),
            seed_spec=spec,
            use_fast_model=False,
            sync_cloud=True,
        )
    return results


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    jobs = ensure_precomputed_demo_jobs(force=True)
    for jid, jdata in jobs.items():
        print(
            f"Job {jid}: status={jdata['status']}, "
            f"Signal1={jdata['verification']['signal_1_chart_validator']['status']}, "
            f"Signal2={jdata['verification']['signal_2_playwright_autoplayer']['status']}, "
            f"GCS={jdata['gcs']['gcs_synced']}, Firestore={jdata.get('firestore_synced')}"
        )
