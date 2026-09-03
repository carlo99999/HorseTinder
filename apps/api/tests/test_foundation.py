from pathlib import Path
from uuid import UUID

import pytest
from app.config import ConfigurationError, Settings
from app.db.fixtures import load_fixtures
from app.db.migrations import migrate
from app.db.models import Gesture, HorseProfile, Match
from app.main import create_app
from litestar.testing import TestClient
from sqlalchemy import create_engine, func, inspect, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


@pytest.mark.parametrize("missing_setting", ["DATABASE_URL", "APP_SECRET"])
def test_each_missing_configuration_refuses_startup_with_safe_json_log(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], missing_setting: str
) -> None:
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://user:password@host/database")
    monkeypatch.setenv("APP_SECRET", "do-not-log")
    monkeypatch.delenv(missing_setting)
    with pytest.raises(ConfigurationError, match=missing_setting):
        create_app()
    stderr = capsys.readouterr().err
    assert '"event": "startup_failure"' in stderr
    assert '"code": "configuration_invalid"' in stderr
    assert "do-not-log" not in stderr


def test_health_and_non_versioned_routes_use_json_contract_and_request_event(
    capsys: pytest.CaptureFixture[str],
) -> None:
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
    stderr = capsys.readouterr().err
    assert '"event": "request"' in stderr
    assert '"method": "GET"' in stderr
    assert '"path": "/api/v1/health"' in stderr


def test_database_prepare_failure_logs_structured_startup_event(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
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
    stderr = capsys.readouterr().err
    assert '"event": "startup_failure"' in stderr
    assert '"code": "database_prepare_failed"' in stderr
    assert "database-password" not in stderr
    assert "do-not-log-this" not in stderr


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
        assert session.scalar(
            select(HorseProfile.id).where(HorseProfile.display_name == "Clover Comet")
        ) == UUID("11111111-1111-4111-8111-111111111111")
    columns = {column["name"] for column in inspect(engine).get_columns("horse_profiles")}
    assert {"account_id", "updated_at"}.issubset(columns)


def test_cli_prepares_a_database(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    from app.cli import prepare_database

    database_path = tmp_path / "prepared.sqlite"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{database_path}")
    monkeypatch.setenv("APP_SECRET", "test-only")
    prepare_database()
    engine = create_engine(f"sqlite:///{database_path}")
    with Session(engine) as session:
        assert session.scalar(select(func.count()).select_from(HorseProfile)) == 2


def test_persistence_constraints_reject_noncanonical_and_self_references() -> None:
    engine = create_engine("sqlite:///:memory:")
    migrate(engine)
    load_fixtures(engine)
    with Session(engine) as session:
        clover, juniper = session.scalars(
            select(HorseProfile).order_by(HorseProfile.display_name)
        ).all()
        session.add(Match(first_profile_id=juniper.id, second_profile_id=clover.id))
        with pytest.raises(IntegrityError):
            session.flush()
        session.rollback()
        session.add(Gesture(from_profile_id=clover.id, to_profile_id=clover.id, kind="neigh"))
        with pytest.raises(IntegrityError):
            session.flush()
