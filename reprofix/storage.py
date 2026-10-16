"""Dual-Mode Storage (Local JSON + Cloud Firestore + Cloud Storage) for ReproFix."""
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv

os.environ.setdefault("GRPC_ENABLE_FORK_SUPPORT", "1")
os.environ.setdefault("GRPC_POLL_STRATEGY", "poll")
os.environ.setdefault("OBJC_DISABLE_INITIALIZE_FORK_SAFETY", "YES")

BASE_DIR = Path(__file__).resolve().parent
ROOT_ENV = BASE_DIR.parent / ".env"
if ROOT_ENV.exists():
    load_dotenv(ROOT_ENV, override=False)

DATA_DIR = BASE_DIR / "data"
JOBS_DIR = DATA_DIR / "jobs"
SANDBOXES_DIR = DATA_DIR / "sandboxes"
RECORDINGS_DIR = DATA_DIR / "recordings"

for d in (DATA_DIR, JOBS_DIR, SANDBOXES_DIR, RECORDINGS_DIR):
    d.mkdir(parents=True, exist_ok=True)

GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "h2gdm-hack26icn-2655")
GCS_BUCKET_NAME = os.environ.get("GCS_BUCKET_NAME", "h2gdm-hack26icn-2655-assets")
FIRESTORE_COLLECTION = "reprofix_jobs"

_gcs_client = None


def get_gcs_bucket():
    """GCS uses pure HTTP/REST (requests), so it is 100% fork-safe with ffmpeg/Playwright."""
    global _gcs_client
    try:
        from google.cloud import storage
        if _gcs_client is None:
            _gcs_client = storage.Client(project=GCP_PROJECT_ID)
        return _gcs_client.bucket(GCS_BUCKET_NAME)
    except Exception as exc:
        print(f"[storage] GCS fallback to local-only: {exc}")
        return None


def _sync_job_file_to_firestore_isolated(job_id: str, job_file: Path) -> Optional[str]:
    """
    Runs Firestore gRPC document write in an isolated child process so the parent FastAPI /
    Playwright process never initializes C-core gRPC poll threads across subsequent forks.
    """
    code = (
        "import json, sys\n"
        "from google.cloud import firestore\n"
        "project_id, coll, doc_id, fpath = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]\n"
        "data = json.loads(open(fpath, encoding='utf-8').read())\n"
        "db = firestore.Client(project=project_id)\n"
        "db.collection(coll).document(doc_id).set(data)\n"
    )
    try:
        proc = subprocess.run(
            [sys.executable, "-c", code, GCP_PROJECT_ID, FIRESTORE_COLLECTION, job_id, str(job_file)],
            capture_output=True,
            text=True,
            timeout=25,
            env=os.environ.copy(),
        )
        if proc.returncode == 0:
            return f"projects/{GCP_PROJECT_ID}/databases/(default)/documents/{FIRESTORE_COLLECTION}/{job_id}"
        print(f"[storage] Firestore isolated sync warning: {proc.stderr.strip()[:160]}")
    except Exception as exc:
        print(f"[storage] Firestore isolated sync warning: {exc}")
    return None


def job_dir(job_id: str) -> Path:
    d = JOBS_DIR / job_id
    d.mkdir(parents=True, exist_ok=True)
    return d


def upload_artifact_to_gcs(job_id: str, local_path: Path, content_type: Optional[str] = None) -> Optional[str]:
    """Uploads a local artifact to GCS under reprofix/<job_id>/<filename> and returns gs:// URI."""
    if not local_path.exists():
        return None
    bucket = get_gcs_bucket()
    if bucket is None:
        return None
    try:
        blob_name = f"reprofix/{job_id}/{local_path.name}"
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(str(local_path), content_type=content_type)
        return f"gs://{GCS_BUCKET_NAME}/{blob_name}"
    except Exception as exc:
        print(f"[storage] GCS upload warning for {local_path.name}: {exc}")
        return None


def save_job(job_data: Dict[str, Any], sync_cloud: bool = True) -> Dict[str, Any]:
    """Saves job state locally and optionally syncs to Cloud Firestore."""
    job_id = job_data["job_id"]
    job_data["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    jdir = job_dir(job_id)
    job_file = jdir / "job.json"

    job_file.write_text(json.dumps(job_data, indent=2, ensure_ascii=False), encoding="utf-8")

    if sync_cloud:
        fs_path = _sync_job_file_to_firestore_isolated(job_id, job_file)
        if fs_path:
            job_data.setdefault("cloud_sync", {})["firestore"] = fs_path
            job_data["cloud_sync"]["synced_at"] = job_data["updated_at"]
            job_file.write_text(json.dumps(job_data, indent=2, ensure_ascii=False), encoding="utf-8")

    return job_data


def load_job(job_id: str) -> Optional[Dict[str, Any]]:
    """Loads job state from local disk."""
    job_file = JOBS_DIR / job_id / "job.json"
    if job_file.exists():
        return json.loads(job_file.read_text(encoding="utf-8"))
    return None


def list_jobs() -> List[Dict[str, Any]]:
    """Lists all jobs ordered by created_at descending."""
    jobs = []
    if JOBS_DIR.exists():
        for child in sorted(JOBS_DIR.iterdir(), reverse=True):
            jf = child / "job.json"
            if jf.exists():
                try:
                    jobs.append(json.loads(jf.read_text(encoding="utf-8")))
                except Exception:
                    pass
    jobs.sort(key=lambda j: j.get("created_at", ""), reverse=True)
    return jobs


def append_job_log(job_id: str, phase: str, message: str, status: str = "INFO", sync_cloud: bool = True) -> Dict[str, Any]:
    """Appends a timestamped log entry to the job's timeline and saves."""
    job = load_job(job_id)
    if not job:
        raise ValueError(f"Job {job_id} not found")
    entry = {
        "timestamp": time.strftime("%H:%M:%S", time.gmtime()),
        "phase": phase,
        "status": status,
        "message": message,
    }
    job.setdefault("logs", []).append(entry)
    return save_job(job, sync_cloud=sync_cloud)
