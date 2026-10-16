import json
from pathlib import Path
from typing import Dict, Any, List, Optional

from .config import (
    GCP_PROJECT_ID,
    GCS_BUCKET_NAME,
    FIRESTORE_DATABASE,
    FIRESTORE_COLLECTION,
    JOBS_DIR,
)
from .schemas import JobRecord


def save_job_local(job: JobRecord) -> Path:
    job_dir = JOBS_DIR / job.job_id
    job_dir.mkdir(parents=True, exist_ok=True)
    meta_path = job_dir / "job.json"
    meta_path.write_text(job.model_dump_json(indent=2), encoding="utf-8")
    return meta_path


def load_job_local(job_id: str) -> Optional[JobRecord]:
    meta_path = JOBS_DIR / job_id / "job.json"
    if not meta_path.exists():
        return None
    try:
        return JobRecord.model_validate_json(meta_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[Storage] Failed to load job {job_id}: {e}")
        return None


def list_jobs_local() -> List[JobRecord]:
    jobs: List[JobRecord] = []
    if not JOBS_DIR.exists():
        return jobs
    for d in sorted(JOBS_DIR.iterdir(), key=lambda p: p.name):
        if d.is_dir():
            j = load_job_local(d.name)
            if j:
                jobs.append(j)
    # Sort demo jobs first, then newest created_at
    jobs.sort(key=lambda x: (0 if x.job_id.startswith("demo_") else 1, x.created_at), reverse=False)
    return jobs


def sync_job_to_cloud(job: JobRecord) -> JobRecord:
    """Uploads scene & proxy artifacts to GCS and syncs job metadata to Firestore."""
    job_dir = JOBS_DIR / job.job_id
    gcs_urls: Dict[str, str] = {}

    # 1. Upload key files to GCS bucket
    try:
        from google.cloud import storage

        storage_client = storage.Client(project=GCP_PROJECT_ID)
        bucket = storage_client.bucket(GCS_BUCKET_NAME)

        files_to_upload = [
            ("job.json", job_dir / "job.json", "application/json"),
            ("scene/index.html", job_dir / "scene" / "index.html", "text/html"),
            ("scene/scene.js", job_dir / "scene" / "scene.js", "application/javascript"),
            ("scene/score.json", job_dir / "scene" / "score.json", "application/json"),
            ("scene/sprites.png", job_dir / "scene" / "sprites.png", "image/png"),
            ("scene/sprites_chromakey_raw.png", job_dir / "scene" / "sprites_chromakey_raw.png", "image/png"),
        ]
        # Also upload proxy verification frames
        verify_dir = job_dir / "verification"
        if verify_dir.exists():
            for png in verify_dir.glob("*.png"):
                files_to_upload.append((f"verification/{png.name}", png, "image/png"))

        for rel_key, local_path, content_type in files_to_upload:
            if local_path.exists():
                blob_name = f"musico/{job.job_id}/{rel_key}"
                blob = bucket.blob(blob_name)
                blob.upload_from_filename(str(local_path), content_type=content_type, timeout=20)
                gcs_urls[rel_key] = f"gs://{GCS_BUCKET_NAME}/{blob_name}"
    except Exception as e:
        print(f"[Storage] GCS upload note for {job.job_id}: {e}")

    job.gcs_urls = gcs_urls

    # 2. Sync job document to Firestore
    try:
        from google.cloud import firestore

        db = firestore.Client(project=GCP_PROJECT_ID, database=FIRESTORE_DATABASE)
        doc_ref = db.collection(FIRESTORE_COLLECTION).document(job.job_id)
        payload = json.loads(job.model_dump_json())
        doc_ref.set(payload)
        job.firestore_synced = True
    except Exception as e:
        print(f"[Storage] Firestore sync note for {job.job_id}: {e}")

    save_job_local(job)
    return job
