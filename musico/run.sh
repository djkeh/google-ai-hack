#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

export PATH="/Users/uno/Downloads/google-cloud-sdk/bin:$PATH"
export PYTHONPATH="${ROOT_DIR}"

VENV_PY="${ROOT_DIR}/.venv/bin/python"
if [ ! -x "${VENV_PY}" ]; then
  VENV_PY="python3"
fi

echo "[Musico] Ensuring pre-computed demo tracks & verification logs..."
"${VENV_PY}" -m musico.pipeline

echo "[Musico] Starting FastAPI Studio Server on http://0.0.0.0:${MUSICO_PORT:-8001} ..."
exec "${VENV_PY}" -m uvicorn musico.app:app --host 0.0.0.0 --port "${MUSICO_PORT:-8001}"
