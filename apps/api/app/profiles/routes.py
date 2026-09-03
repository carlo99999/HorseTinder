"""Authenticated, owner-scoped Horse Profile endpoints."""

from typing import Any

from litestar import Request, Response, get, post, put

from app.auth.services import (
    CSRF_HEADER,
    SESSION_COOKIE,
    AuthError,
    AuthService,
    valid_session_csrf,
)
from app.profiles.services import ProfileError, ProfileService, profile_dto


def _service(request: Request[Any, Any, Any]) -> AuthService:
    return AuthService(request.app.state.settings, request.app.state.auth_engine)


def _profiles(request: Request[Any, Any, Any]) -> ProfileService:
    return ProfileService(request.app.state.auth_engine)


def _error(exc: ProfileError | AuthError) -> Response:
    from app.main import error_response

    return error_response(exc.code, exc.message, exc.status_code, getattr(exc, "details", None))


def _actor(request: Request[Any, Any, Any], *, csrf_required: bool) -> tuple[Any, Any]:
    token = request.cookies.get(SESSION_COOKIE)
    actor, account = _service(request).actor(token)
    csrf = request.headers.get(CSRF_HEADER)
    if csrf_required and (not token or not valid_session_csrf(actor, token, csrf)):
        raise ProfileError("csrf_invalid", "A fresh security token is required.", 403)
    return actor, account


@get("/api/v1/profiles/me")
async def get_my_profile(request: Request[Any, Any, Any]) -> Response:
    try:
        _, account = _actor(request, csrf_required=False)
        return Response(
            content={"data": profile_dto(_profiles(request).get(account.id))},
            headers={"Cache-Control": "no-store"},
        )
    except (AuthError, ProfileError) as exc:
        return _error(exc)


async def _payload(request: Request[Any, Any, Any]) -> Any:
    try:
        return await request.json()
    except Exception as exc:
        raise ProfileError(
            "validation_failed", "Enter your profile details.", 422, _field_details()
        ) from exc


def _field_details() -> dict[str, str]:
    return {field: "Enter a valid value." for field in ("displayName", "imageUrl", "bio", "trait")}


@post("/api/v1/profiles/me")
async def create_my_profile(request: Request[Any, Any, Any]) -> Response:
    try:
        _, account = _actor(request, csrf_required=True)
        profile = _profiles(request).create(account.id, await _payload(request))
        return Response(content={"data": profile_dto(profile)}, status_code=201)
    except (AuthError, ProfileError) as exc:
        return _error(exc)


@put("/api/v1/profiles/me")
async def update_my_profile(request: Request[Any, Any, Any]) -> Response:
    try:
        _, account = _actor(request, csrf_required=True)
        profile = _profiles(request).update(account.id, await _payload(request))
        return Response(content={"data": profile_dto(profile)})
    except (AuthError, ProfileError) as exc:
        return _error(exc)
