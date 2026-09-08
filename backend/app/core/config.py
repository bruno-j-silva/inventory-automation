from pathlib import Path
from typing import Literal

from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="APP_", extra="ignore")

    environment: Literal["development", "test", "production"] = "development"
    db_host: str = "localhost"
    db_port: int = Field(default=5432, ge=1, le=65535)
    db_name: str = "inventory"
    db_user: str = "inventory_app"
    db_password: SecretStr | None = None
    db_password_file: Path | None = None

    @model_validator(mode="after")
    def require_password(self) -> "Settings":
        if (self.db_password is None) == (self.db_password_file is None):
            raise ValueError(
                "Configure uma fonte de senha: APP_DB_PASSWORD ou APP_DB_PASSWORD_FILE."
            )
        if self.db_password_file is not None:
            self.db_password = SecretStr(self.db_password_file.read_text().strip())
        if self.db_password is None or not self.db_password.get_secret_value():
            raise ValueError("A senha de conexão não pode estar vazia.")
        return self

    def database_url(self) -> URL:
        assert self.db_password is not None
        return URL.create(
            "postgresql+psycopg",
            username=self.db_user,
            password=self.db_password.get_secret_value(),
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
        )
