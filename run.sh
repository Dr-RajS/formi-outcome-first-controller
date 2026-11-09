#!/usr/bin/env bash
set -euo pipefail
SIM_URL="${1:?usage: ./run.sh <SIM_URL>}"
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
exec python controller.py --url "$SIM_URL" --db "${CONTROLLER_DB:-controller_state.sqlite3}"
