#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
export PATH="/Users/uno/Downloads/google-cloud-sdk/bin:$PATH"

VENV_PYTHON="/Users/uno/Documents/github/google-ai-hack/.venv/bin/python"
if [ ! -x "$VENV_PYTHON" ]; then
  VENV_PYTHON="python3"
fi

export PORT="${PORT:-8002}"
echo "[YourDancer] Ensuring seed dance practice videos & precomputed charts..."
"$VENV_PYTHON" seed_video.py

echo "[YourDancer] Starting FastAPI Studio Server on http://127.0.0.1:${PORT} ..."
exec "$VENV_PYTHON" app.py
