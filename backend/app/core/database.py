from typing import Protocol

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import Settings


class DatabaseProbe(Protocol):
    def ready(self) -> bool: ...
    def close(self) -> None: ...


class PostgresProbe:
    def __init__(self, settings: Settings) -> None:
        self.engine = create_engine(
            settings.database_url(),
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=5,
            pool_timeout=3,
            connect_args={"connect_timeout": 3, "options": "-c statement_timeout=3000"},
        )

    def ready(self) -> bool:
        try:
            with self.engine.connect() as connection:
                return bool(connection.execute(text("SELECT 1")).scalar_one() == 1)
        except SQLAlchemyError:
            return False

    def close(self) -> None:
        self.engine.dispose()
