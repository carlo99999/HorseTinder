from app.db.models import HorseProfile
from sqlalchemy import select
from sqlalchemy.orm import Session
from test_auth import app_client, csrf, register

PROFILE = {
    "displayName": "Marevel",
    "imageUrl": "https://example.test/marevel.jpg",
    "bio": "A gentle canter and excellent puns.",
    "trait": "Stargazer",
}


def create(client, profile=PROFILE):
    csrf = register(client)["csrfToken"]
    return client.post("/api/v1/profiles/me", headers={"X-CSRF-Token": str(csrf)}, json=profile)


def test_owner_can_create_read_and_update_only_public_profile_fields() -> None:
    with app_client() as client:
        created = create(client)
        assert created.status_code == 201
        data = created.json()["data"]
        assert set(data) == {
            "id",
            "displayName",
            "imageUrl",
            "bio",
            "trait",
            "createdAt",
            "updatedAt",
        }
        assert data["displayName"] == PROFILE["displayName"]
        csrf = client.get("/api/v1/auth/session").json()["data"]["csrfToken"]
        edited = {**PROFILE, "trait": "Trailblazer"}
        assert (
            client.put(
                "/api/v1/profiles/me", headers={"X-CSRF-Token": csrf}, json=edited
            ).status_code
            == 200
        )
        read = client.get("/api/v1/profiles/me")
        assert read.headers["cache-control"] == "no-store"
        assert read.json()["data"]["trait"] == "Trailblazer"
        csrf = register(client, "other@example.test")["csrfToken"]
        assert client.get("/api/v1/profiles/me").status_code == 404
        updated = client.put(
            "/api/v1/profiles/me", headers={"X-CSRF-Token": str(csrf)}, json=PROFILE
        )
        assert updated.status_code == 404


def test_profile_validates_all_fields_and_requires_session_csrf() -> None:
    with app_client() as client:
        csrf_token = register(client)["csrfToken"]
        denied = client.post("/api/v1/profiles/me", json=PROFILE)
        assert denied.status_code == 403
        invalid = client.post(
            "/api/v1/profiles/me", headers={"X-CSRF-Token": str(csrf_token)}, json={}
        )
        assert invalid.status_code == 422
        assert set(invalid.json()["details"]) == {"displayName", "imageUrl", "bio", "trait"}
        malformed = client.post(
            "/api/v1/profiles/me", headers={"X-CSRF-Token": str(csrf_token)}, content="["
        )
        assert malformed.status_code == 422
        assert set(malformed.json()["details"]) == {"displayName", "imageUrl", "bio", "trait"}
        non_object = client.post(
            "/api/v1/profiles/me", headers={"X-CSRF-Token": str(csrf_token)}, json=[]
        )
        assert set(non_object.json()["details"]) == {"displayName", "imageUrl", "bio", "trait"}
        bad_url = client.post(
            "/api/v1/profiles/me",
            headers={"X-CSRF-Token": str(csrf_token)},
            json={**PROFILE, "imageUrl": "https:///missing-host"},
        )
        assert bad_url.json()["details"]["imageUrl"]


def test_one_profile_constraint_and_persistence() -> None:
    with app_client() as client:
        assert create(client).status_code == 201
        csrf = client.get("/api/v1/auth/session").json()["data"]["csrfToken"]
        duplicate = client.post("/api/v1/profiles/me", headers={"X-CSRF-Token": csrf}, json=PROFILE)
        assert duplicate.status_code == 409
        with Session(client.app.state.auth_engine) as db:
            owned = db.scalars(
                select(HorseProfile).where(HorseProfile.account_id.is_not(None))
            ).all()
            assert len(owned) == 1


def test_profile_survives_a_new_authenticated_session() -> None:
    with app_client() as client:
        assert create(client).status_code == 201
        session_csrf = client.get("/api/v1/auth/session").json()["data"]["csrfToken"]
        assert (
            client.post("/api/v1/auth/sign-out", headers={"X-CSRF-Token": session_csrf}).status_code
            == 204
        )
        signed_in = client.post(
            "/api/v1/auth/sign-in",
            headers={"X-CSRF-Token": csrf(client)},
            json={"email": "rider@example.test", "password": "a safe horse password"},
        )
        assert signed_in.status_code == 200
        response = client.get("/api/v1/profiles/me")
        assert response.status_code == 200
        assert response.json()["data"]["displayName"] == PROFILE["displayName"]
        assert signed_in.json()["data"]["csrfToken"]
