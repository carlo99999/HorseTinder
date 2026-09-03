from datetime import UTC, datetime, timedelta

from app.config import Settings
from app.db.models import AccountSession
from app.main import create_app
from litestar.testing import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session


def app_client() -> TestClient:
    return TestClient(create_app(Settings("sqlite:///:memory:", "test-secret")))


def csrf(client: TestClient) -> str:
    response = client.get("/api/v1/auth/csrf")
    assert response.status_code == 200
    return response.json()["data"]["csrfToken"]


def register(client: TestClient, email: str = "rider@example.test") -> dict[str, object]:
    response = client.post(
        "/api/v1/auth/register",
        headers={"X-CSRF-Token": csrf(client)},
        json={"email": email, "password": "a safe horse password"},
    )
    assert response.status_code == 200
    return response.json()["data"]


def test_anonymous_csrf_is_required_for_registration_and_sign_in() -> None:
    with app_client() as client:
        response = client.post(
            "/api/v1/auth/register",
            json={"email": "rider@example.test", "password": "a safe horse password"},
        )
        assert response.status_code == 403
        assert response.json()["code"] == "csrf_invalid"
        response = client.post(
            "/api/v1/auth/sign-in",
            json={"email": "rider@example.test", "password": "a safe horse password"},
        )
        assert response.status_code == 403
        assert response.json()["code"] == "csrf_invalid"


def test_registration_creates_cookie_session_and_protected_actor_is_server_derived() -> None:
    with app_client() as client:
        data = register(client)
        assert data["authenticated"] is True
        assert "csrfToken" in data
        assert "HttpOnly" in client.cookies.get("horse_tinder_session", "") or client.cookies.get(
            "horse_tinder_session"
        )
        response = client.get("/api/v1/auth/session")
        assert response.status_code == 200
        assert response.json()["data"] == {"authenticated": True, "csrfToken": data["csrfToken"]}


def test_duplicate_registration_is_neutral_and_does_not_create_another_session() -> None:
    with app_client() as client:
        register(client)
        response = client.post(
            "/api/v1/auth/register",
            headers={"X-CSRF-Token": csrf(client)},
            json={"email": "rider@example.test", "password": "a safe horse password"},
        )
        assert response.status_code == 400
        assert response.json() == {
            "code": "registration_failed",
            "message": "We could not create that account.",
        }


def test_sign_in_failure_is_generic_for_unknown_and_wrong_password() -> None:
    with app_client() as client:
        register(client)
        unknown = client.post(
            "/api/v1/auth/sign-in",
            headers={"X-CSRF-Token": csrf(client)},
            json={"email": "unknown@example.test", "password": "a safe horse password"},
        )
        wrong = client.post(
            "/api/v1/auth/sign-in",
            headers={"X-CSRF-Token": csrf(client)},
            json={"email": "rider@example.test", "password": "wrong safe password"},
        )
        assert (
            unknown.json()
            == wrong.json()
            == {"code": "authentication_failed", "message": "Email or password is incorrect."}
        )


def test_missing_protected_session_is_denied() -> None:
    with app_client() as client:
        response = client.get("/api/v1/auth/session")
        assert response.status_code == 401
        assert response.json()["code"] == "unauthorized"


def test_sign_out_requires_session_csrf_and_revokes_the_active_session() -> None:
    with app_client() as client:
        data = register(client)
        denied = client.post("/api/v1/auth/sign-out")
        assert denied.status_code == 403
        assert denied.json()["code"] == "csrf_invalid"
        signed_out = client.post(
            "/api/v1/auth/sign-out", headers={"X-CSRF-Token": str(data["csrfToken"])}
        )
        assert signed_out.status_code == 204
        assert client.get("/api/v1/auth/session").status_code == 401


def test_expired_session_is_denied() -> None:
    with app_client() as client:
        register(client)
        with Session(client.app.state.auth_engine) as db:
            session = db.scalar(select(AccountSession))
            assert session is not None
            session.expires_at = datetime.now(UTC) - timedelta(seconds=1)
            db.commit()
        response = client.get("/api/v1/auth/session")
        assert response.status_code == 401
        assert response.json()["code"] == "unauthorized"
