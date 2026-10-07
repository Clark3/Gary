#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "$0")" && pwd)"
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
python3 "$ROOT/src/gary/cli.py" status
if ! command -v llama-server >/dev/null 2>&1; then
  echo 'Gary runtime is not fully configured yet: llama-server was not found.'
  echo 'This MVP performs preflight only; on-demand LLM lifecycle is a later phase.'
  exit 0
fi
echo 'llama-server detected. Model orchestration is reserved for the model-manager phase.'
