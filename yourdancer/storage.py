import json
import logging
import shutil
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from config import (
    FIRESTORE_COLLECTION,
    FIRESTORE_DATABASE,
    GCP_PROJECT_ID,
    GCS_BUCKET_NAME,
    JOBS_DIR,
)

logger = logging.getLogger("yourdancer.storage")


class DualStorage:
    """Dual-mode storage: always writes to local disk and syncs to Firestore + GCS when available."""

    def __init__(self) -> None:
        self._fs_client = None
        self._gcs_client = None
        self._fs_init_tried = False
        self._gcs_init_tried = False

    @property
    def firestore_client(self):
        if not self._fs_init_tried:
            self._fs_init_tried = True
            try:
                from google.cloud import firestore

                self._fs_client = firestore.Client(
                    project=GCP_PROJECT_ID,
                    database=FIRESTORE_DATABASE,
                )
            except Exception as exc:
                logger.warning("Firestore init skipped: %s", exc)
                self._fs_client = None
        return self._fs_client

    @property
    def gcs_client(self):
        if not self._gcs_init_tried:
            self._gcs_init_tried = True
            try:
                from google.cloud import storage

                self._gcs_client = storage.Client(project=GCP_PROJECT_ID)
            except Exception as exc:
                logger.warning("GCS init skipped: %s", exc)
                self._gcs_client = None
        return self._gcs_client

    def job_dir(self, job_id: str) -> Path:
        d = JOBS_DIR / job_id
        d.mkdir(parents=True, exist_ok=True)
        return d

    def save_job(self, job_id: str, job_data: Dict[str, Any], sync_cloud: bool = True) -> Dict[str, Any]:
        job_data["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        jdir = self.job_dir(job_id)
        job_file = jdir / "job.json"
        job_file.write_text(json.dumps(job_data, indent=2, ensure_ascii=False), encoding="utf-8")

        if sync_cloud and self.firestore_client is not None:
            try:
                doc_ref = self.firestore_client.collection(FIRESTORE_COLLECTION).document(job_id)
                doc_ref.set(job_data, merge=True)
                job_data["firestore_synced"] = True
                job_file.write_text(json.dumps(job_data, indent=2, ensure_ascii=False), encoding="utf-8")
            except Exception as exc:
                logger.warning("Firestore sync failed for %s: %s", job_id, exc)
                job_data.setdefault("firestore_synced", False)
        return job_data

    def load_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        job_file = JOBS_DIR / job_id / "job.json"
        if job_file.exists():
            try:
                return json.loads(job_file.read_text(encoding="utf-8"))
            except Exception as exc:
                logger.error("Failed reading local job %s: %s", job_id, exc)
        if self.firestore_client is not None:
            try:
                doc = self.firestore_client.collection(FIRESTORE_COLLECTION).document(job_id).get()
                if doc.exists:
                    return doc.to_dict()
            except Exception as exc:
                logger.warning("Firestore read failed for %s: %s", job_id, exc)
        return None

    def list_jobs(self) -> List[Dict[str, Any]]:
        jobs: List[Dict[str, Any]] = []
        if JOBS_DIR.exists():
            for child in sorted(JOBS_DIR.iterdir()):
                if child.is_dir() and (child / "job.json").exists():
                    try:
                        data = json.loads((child / "job.json").read_text(encoding="utf-8"))
                        jobs.append(data)
                    except Exception:
                        pass
        jobs.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return jobs

    def sync_directory_to_gcs(self, job_id: str, local_dir: Path, prefix_subpath: str = "") -> Dict[str, Any]:
        """Uploads files in local_dir to gs://<bucket>/yourdancer/<job_id>/<prefix_subpath>."""
        result = {
            "bucket": GCS_BUCKET_NAME,
            "gcs_prefix": f"gs://{GCS_BUCKET_NAME}/yourdancer/{job_id}/{prefix_subpath}".rstrip("/"),
            "uploaded_files": [],
            "gcs_synced": False,
        }
        if self.gcs_client is None:
            return result
        try:
            bucket = self.gcs_client.bucket(GCS_BUCKET_NAME)
            for file_path in sorted(local_dir.rglob("*")):
                if not file_path.is_file():
                    continue
                rel = file_path.relative_to(local_dir).as_posix()
                blob_name = f"yourdancer/{job_id}/{prefix_subpath}/{rel}".replace("//", "/").strip("/")
                blob = bucket.blob(blob_name)
                content_type = None
                if file_path.suffix == ".html":
                    content_type = "text/html; charset=utf-8"
                elif file_path.suffix == ".js":
                    content_type = "application/javascript; charset=utf-8"
                elif file_path.suffix == ".json":
                    content_type = "application/json; charset=utf-8"
                elif file_path.suffix == ".mp4":
                    content_type = "video/mp4"
                elif file_path.suffix == ".png":
                    content_type = "image/png"
                blob.upload_from_filename(str(file_path), content_type=content_type)
                result["uploaded_files"].append(f"gs://{GCS_BUCKET_NAME}/{blob_name}")
            result["gcs_synced"] = len(result["uploaded_files"]) > 0
        except Exception as exc:
            logger.warning("GCS upload failed for job %s: %s", job_id, exc)
            result["error"] = str(exc)
        return result


storage_manager = DualStorage()
