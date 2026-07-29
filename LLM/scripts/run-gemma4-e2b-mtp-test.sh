#!/usr/bin/env bash
# Gemma 4 E2B + MTP smoke test via llama-server (llama-cli lacks --spec-type).
set -euo pipefail

ROOT="/e/IT_SPACES/AI/ZoomCamp/LLM"
ATOMIC="${ROOT}/atomic-llama-cpp-turboquant"
SERVER="${ATOMIC}/build/bin/llama-server.exe"
MODEL_DIR="${ROOT}/models/gemma-4-e2b"

MAIN="${MAIN_GGUF:-${MODEL_DIR}/gemma-4-E2B-it-Q4_K_M.gguf}"
DRAFT="${DRAFT_GGUF:-${MODEL_DIR}/gemma-4-E2B-it-assistant.Q4_K_M.gguf}"
PROMPT="${PROMPT:-hello}"
N_PREDICT="${N_PREDICT:-32}"
CTX="${CTX:-4096}"
HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-8081}"

if [[ ! -f "$SERVER" ]]; then
  echo "error: llama-server not found: ${SERVER}" >&2
  echo "hint: bash ${ROOT}/scripts/build-atomic-llama-cpp.sh" >&2
  exit 1
fi
if [[ ! -f "$MAIN" || ! -f "$DRAFT" ]]; then
  echo "error: model files missing under ${MODEL_DIR}" >&2
  echo "hint: python ${ROOT}/scripts/download-gemma4-e2b-models.py" >&2
  exit 1
fi

echo "=== Gemma 4 E2B MTP smoke test (CPU, llama-server) ==="
echo "SERVER: ${SERVER}"
echo "MAIN:   ${MAIN}"
echo "DRAFT:  ${DRAFT}"
echo "PROMPT: ${PROMPT}"
echo ""

"$SERVER" \
  -m "$MAIN" \
  --mtp-head "$DRAFT" \
  --spec-type mtp \
  --draft-block-size 2 \
  --draft-max 6 \
  -c "$CTX" \
  -ngl 0 \
  -ngld 0 \
  -ctk turbo3 \
  -ctv turbo3 \
  -ctkd turbo3 \
  -ctvd turbo3 \
  --host "$HOST" \
  --port "$PORT" \
  --parallel 1 \
  -np 1 \
  --cont-batching \
  --no-warmup \
  "$@" &

SERVER_PID=$!
trap 'kill "$SERVER_PID" 2>/dev/null || true' EXIT

echo "waiting for server on http://${HOST}:${PORT} ..."
for _ in $(seq 1 120); do
  if curl -sf "http://${HOST}:${PORT}/health" >/dev/null 2>&1; then
    break
  fi
  sleep 2
done

curl -sf "http://${HOST}:${PORT}/health" >/dev/null || {
  echo "error: server did not become ready" >&2
  exit 1
}

echo ""
echo "=== completion ==="
curl -sf "http://${HOST}:${PORT}/completion" \
  -H "Content-Type: application/json" \
  -d "{\"prompt\":\"${PROMPT}\",\"n_predict\":${N_PREDICT},\"temperature\":0}" \
  | python -m json.tool

echo ""
echo "=== done ==="
