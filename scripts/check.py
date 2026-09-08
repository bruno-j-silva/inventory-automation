"""Run the verified foundation checks without requiring Make."""

import argparse
import os
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--part", choices=("all", "backend", "frontend"), default="all")
args = parser.parse_args()
environment = dict(os.environ, UV_CACHE_DIR=str(root / ".local/uv-cache"))
uv = os.environ.get("UV", str(root / ".local/bin/uv"))
if args.part in ("all", "backend"):
    for command in (
        ["ruff", "check", "."],
        ["ruff", "format", "--check", "."],
        ["mypy"],
        ["pytest"],
    ):
        subprocess.run([uv, "run", "--frozen", *command], cwd=root / "backend",
                       env=environment, check=True, timeout=120)
if args.part in ("all", "frontend"):
    for task in ("lint", "format:check", "test", "build"):
        subprocess.run(["npm", "run", task], cwd=root / "frontend", check=True, timeout=120)
