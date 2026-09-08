"""Copy a mounted secret privately, then drop privileges before starting the API."""

import os
import sys
from pathlib import Path

if os.getuid() == 0:
    source = Path(os.environ["APP_DB_PASSWORD_FILE"])
    directory = Path("/run/inventory")
    directory.mkdir(mode=0o700, exist_ok=True)
    os.chown(directory, 10001, 10001)
    target = directory / "db_password"
    descriptor = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o400)
    with os.fdopen(descriptor, "wb") as stream:
        stream.write(source.read_bytes())
    os.chown(target, 10001, 10001)
    os.chmod(target, 0o400)
    os.environ["APP_DB_PASSWORD_FILE"] = str(target)
    os.setgroups([])
    os.setgid(10001)
    os.setuid(10001)

os.execv(
    sys.executable,
    [
        sys.executable,
        "-m",
        "uvicorn",
        "app.main:create_app",
        "--factory",
        "--host",
        "0.0.0.0",
        "--port",
        "8000",
        "--no-access-log",
    ],
)
