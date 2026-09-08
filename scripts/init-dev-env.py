"""Prepare local Docker configuration without overwriting existing credentials."""

import os
from pathlib import Path
import secrets


def initialize(root: Path) -> None:
    env_path = root / ".env"
    if not env_path.exists():
        with env_path.open("x", encoding="utf-8") as stream:
            stream.write((root / ".env.example").read_text(encoding="utf-8"))
    secret_dir = root / ".local" / "secrets"
    secret_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    for name in ("postgres_password", "app_db_password"):
        password_path = secret_dir / name
        try:
            descriptor = os.open(password_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError:
            continue
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(secrets.token_urlsafe(48))


if __name__ == "__main__":
    initialize(Path(__file__).resolve().parents[1])
    print("Configuração local preparada; arquivos existentes preservados.")
