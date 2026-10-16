import os
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT_DIR / ".env"
if ENV_PATH.exists():
    load_dotenv(ENV_PATH)

LOCAL_ENV_PATH = Path(__file__).resolve().parent / ".env"
if LOCAL_ENV_PATH.exists():
    load_dotenv(LOCAL_ENV_PATH)

# Cloud Run Credential Guard: if GOOGLE_APPLICATION_CREDENTIALS points to a non-existent host path,
# remove it so Cloud Run falls back to its built-in Service Account Application Default Credentials.
_gac = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
if _gac and not Path(_gac).exists():
    os.environ.pop("GOOGLE_APPLICATION_CREDENTIALS", None)
elif not _gac:
    _default_adc = "/Users/uno/.config/gcloud/legacy_credentials/devstar2655@gcplab.me/adc.json"
    if Path(_default_adc).exists():
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = _default_adc

GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "")

YOURDANCER_DIR = Path(__file__).resolve().parent
DATA_DIR = YOURDANCER_DIR / "data"
VIDEOS_DIR = DATA_DIR / "videos"
JOBS_DIR = DATA_DIR / "jobs"
STATIC_DIR = YOURDANCER_DIR / "static"

for _d in (DATA_DIR, VIDEOS_DIR, JOBS_DIR, STATIC_DIR):
    _d.mkdir(parents=True, exist_ok=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-4-argon")
GEMINI_FLASH_MODEL = os.getenv("GEMINI_FLASH_MODEL", "gemini-3.8-flash")
GEMINI_LITE_MODEL = os.getenv("GEMINI_LITE_MODEL", "gemini-3.5-flash-lite")
LYRIA_MODEL = os.getenv("LYRIA_MODEL", "lyria-3.5")

GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "h2gdm-hack26icn-2655")
GCP_REGION = os.getenv("GCP_REGION", "asia-northeast3")
GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME", os.getenv("GCS_BUCKET", "h2gdm-hack26icn-2655-assets"))
FIRESTORE_DATABASE = os.getenv("FIRESTORE_DATABASE", "(default)")
FIRESTORE_COLLECTION = "yourdancer_jobs"

PORT = int(os.getenv("PORT", os.getenv("YOURDANCER_PORT", "8002")))
