import os
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
MUSICO_DIR = Path(__file__).resolve().parent

# Load root .env first, then local .env if present
load_dotenv(ROOT_DIR / ".env")
load_dotenv(MUSICO_DIR / ".env")

# Ensure GOOGLE_APPLICATION_CREDENTIALS is set if file exists
adc_default = "/Users/uno/.config/gcloud/legacy_credentials/devstar2655@gcplab.me/adc.json"
if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") and os.path.exists(adc_default):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = adc_default

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-4-argon")
FLASH_MODEL = os.environ.get("FLASH_MODEL", "gemini-3.8-flash")
FLASH_LITE_MODEL = os.environ.get("FLASH_LITE_MODEL", "gemini-3.5-flash-lite")
NANO_BANANA_MODEL = os.environ.get("NANO_BANANA_MODEL", "gemini-nano-banana-2.1")
TRANSCRIBE_MODEL = os.environ.get("TRANSCRIBE_MODEL", "gemini-3.5-transcribe")

GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "h2gdm-hack26icn-2655")
GCP_REGION = os.environ.get("GCP_REGION", "asia-northeast3")
GCS_BUCKET_NAME = os.environ.get("GCS_BUCKET_NAME", "h2gdm-hack26icn-2655-assets")
FIRESTORE_DATABASE = os.environ.get("FIRESTORE_DATABASE", "(default)")
FIRESTORE_COLLECTION = "musico_jobs"

DATA_DIR = MUSICO_DIR / "data"
DEMO_AUDIO_DIR = DATA_DIR / "demo_audio"
JOBS_DIR = DATA_DIR / "jobs"
STATIC_DIR = MUSICO_DIR / "static"

PORT = int(os.environ.get("MUSICO_PORT", "8001"))

for d in (DATA_DIR, DEMO_AUDIO_DIR, JOBS_DIR, STATIC_DIR):
    d.mkdir(parents=True, exist_ok=True)
