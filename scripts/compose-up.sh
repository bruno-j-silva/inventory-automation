#!/bin/sh
set -eu

root_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$root_dir"

python3 scripts/init-dev-env.py
exec docker compose up -d --build --wait "$@"
