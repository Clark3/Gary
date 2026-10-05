#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "$0")" && pwd)"
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
python3 "$ROOT/src/gary/cli.py" self-test >/dev/null
echo 'Gary MVP has no long-lived runtime to stop yet.'
echo 'Later phases will unload the model, stop llama-server, remove temporary containers, and verify clean shutdown.'
