import json
import logging
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from pydantic import SecretStr, ValidationError

from app.core.config import Settings
from app.core.logging import JsonFormatter
from app.main import create_app


class FakeDatabase:
    def __init__(self, available=True):
        self.available = available
        self.closed = False

    def ready(self):
        return self.available

    def close(self):
        self.closed = True


def settings(**overrides):
    return Settings(environment="test", db_password=SecretStr("test-only"), **overrides)


def test_liveness_survives_database_outage_but_readiness_fails():
    database = FakeDatabase(False)
    with TestClient(create_app(settings(), database)) as client:
        assert client.get("/api/health/live").status_code == 200
        response = client.get("/api/health/ready")
        assert response.status_code == 503
        assert response.json()["error"]["code"] == "SERVICE_UNAVAILABLE"
        assert "test-only" not in response.text
    assert database.closed


def test_readiness_succeeds_only_with_available_database():
    with TestClient(create_app(settings(), FakeDatabase())) as client:
        assert client.get("/api/health/ready").json() == {"status": "ready"}


def test_errors_are_sanitized_and_correlated():
    app = create_app(settings(), FakeDatabase())

    @app.get("/failing")
    def failing():
        raise RuntimeError("private-token-that-must-not-leak")

    with TestClient(app) as client:
        response = client.get("/failing", headers={"X-Request-ID": "demo-123"})
        assert response.status_code == 500
        assert response.json()["error"]["request_id"] == "demo-123"
        assert response.headers["X-Request-ID"] == "demo-123"
        assert "private-token" not in response.text
        assert response.headers["Cache-Control"] == "no-store"


def test_validation_does_not_echo_sensitive_inputs():
    app = create_app(settings(), FakeDatabase())

    @app.get("/typed")
    def typed(count: int):
        return {"count": count}

    with TestClient(app) as client:
        response = client.get("/typed?count=private-token")
        assert response.status_code == 422
        assert "private-token" not in response.text


def test_invalid_request_identifier_is_replaced_and_not_found_is_standardized():
    with TestClient(create_app(settings(), FakeDatabase())) as client:
        response = client.get("/missing", headers={"X-Request-ID": "a" * 100})
        assert response.status_code == 404
        assert len(response.headers["X-Request-ID"]) == 36
        assert response.json()["error"]["code"] == "NOT_FOUND"


def test_password_source_is_required_and_secret_file_supported(tmp_path: Path, monkeypatch):
    monkeypatch.delenv("APP_DB_PASSWORD", raising=False)
    monkeypatch.delenv("APP_DB_PASSWORD_FILE", raising=False)
    with pytest.raises(ValidationError):
        Settings()
    secret_file = tmp_path / "password"
    secret_file.write_text("special@password:/value")
    configuration = Settings(db_password_file=secret_file)
    assert configuration.database_url().password == "special@password:/value"
    assert "special@password" not in repr(configuration)
    with pytest.raises(ValidationError):
        Settings(db_password_file=secret_file, db_password=SecretStr("other"))


def test_documentation_is_not_exposed_in_production():
    config = Settings(environment="production", db_password=SecretStr("test-only"))
    with TestClient(create_app(config, FakeDatabase())) as client:
        assert client.get("/api/docs").status_code == 404
        assert client.get("/api/openapi.json").status_code == 404


def test_log_formatter_does_not_include_exception_or_unapproved_fields():
    record = logging.LogRecord("test", logging.ERROR, "", 0, "http_request", (), None)
    record.password = "private-password"
    record.request_id = "test-request"
    formatted = JsonFormatter().format(record)
    assert json.loads(formatted)["request_id"] == "test-request"
    assert "private-password" not in formatted
