#!/usr/bin/env bash
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

export PATH="/Users/uno/Downloads/google-cloud-sdk/bin:$PATH"
export GRPC_ENABLE_FORK_SUPPORT=1
export GRPC_POLL_STRATEGY=poll
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES

VENV_PY="/Users/uno/Documents/github/google-ai-hack/.venv/bin/python"
if [ ! -x "$VENV_PY" ]; then
  VENV_PY="python3"
fi

PORT="${PORT:-8003}"
echo "[ReproFix] Starting FastAPI server on http://127.0.0.1:${PORT} ..."
exec "$VENV_PY" -m uvicorn app:app --host 127.0.0.1 --port "$PORT"
