import pytest
from app.config import ConfigurationError, Settings
from app.db.fixtures import load_fixtures
from app.db.migrations import migrate
from app.db.models import Gesture, HorseProfile, Match
from app.main import create_app
from litestar.testing import TestClient
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session


def test_missing_configuration_refuses_startup_logs_safe_event(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("APP_SECRET", raising=False)
    with pytest.raises(ConfigurationError, match="DATABASE_URL, APP_SECRET"):
        create_app()
    assert '"event": "startup_failure"' in caplog.text
    assert '"code": "configuration_invalid"' in caplog.text
    assert "APP_SECRET=" not in caplog.text


def test_health_and_non_versioned_routes_use_json_contract() -> None:
    settings = Settings(database_url="sqlite:///:memory:", app_secret="test-only")
    with TestClient(create_app(settings, run_migrations=False)) as client:
        assert client.get("/api/v1/health").json() == {
            "data": {"service": "horse-tinder-api", "version": "v1"}
        }
        response = client.get("/api/v1/no-such-route")
        schema_response = client.get("/schema/openapi.json")
    assert response.status_code == 404
    assert response.json() == {"code": "not_found", "message": "API route was not found."}
    assert schema_response.status_code == 404
    assert schema_response.json() == {"code": "not_found", "message": "API route was not found."}


def test_migration_failure_logs_structured_startup_event(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    settings = Settings(
        database_url="postgresql+psycopg://user:database-password@localhost/example",
        app_secret="do-not-log-this",
    )

    def failed_migration(_: object) -> None:
        raise RuntimeError("database unavailable")

    monkeypatch.setattr("app.main.migrate", failed_migration)
    with pytest.raises(RuntimeError, match="database unavailable"):
        create_app(settings)
    assert '"event": "startup_failure"' in caplog.text
    assert '"code": "migration_failed"' in caplog.text
    assert "database-password" not in caplog.text
    assert "do-not-log-this" not in caplog.text


def test_migrations_and_fixtures_are_repeatable() -> None:
    engine = create_engine("sqlite:///:memory:")
    migrate(engine)
    migrate(engine)
    load_fixtures(engine)
    load_fixtures(engine)
    with Session(engine) as session:
        assert session.scalar(select(func.count()).select_from(HorseProfile)) == 2
        assert session.scalar(select(func.count()).select_from(Match)) == 1
        assert session.scalar(select(func.count()).select_from(Gesture)) == 2
