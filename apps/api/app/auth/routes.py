"""Versioned browser authentication endpoints."""

from typing import Any

from litestar import Request, Response, get, post
from litestar.status_codes import HTTP_204_NO_CONTENT

from app.auth.services import (
    CSRF_HEADER,
    SESSION_COOKIE,
    AuthError,
    AuthService,
    anonymous_csrf_token,
    valid_anonymous_csrf,
    valid_session_csrf,
)
from app.config import Settings


def _settings(request: Request[Any, Any, Any]) -> Settings:
    return request.app.state.settings


def _service(request: Request[Any, Any, Any]) -> AuthService:
    return AuthService(_settings(request), request.app.state.auth_engine)


def _error_response(code: str, message: str, status_code: int) -> Response:
    # Deferred import avoids a module-import cycle while retaining the API-wide error contract.
    from app.main import error_response

    return error_response(code, message, status_code)


def _session_csrf(actor: Any, token: str) -> str:
    import hashlib
    import hmac

    return hmac.new(actor.csrf_secret.encode(), token.encode(), hashlib.sha256).hexdigest()


async def _credentials(request: Request[Any, Any, Any]) -> tuple[str, str]:
    try:
        body = await request.json()
    except ValueError as exc:
        raise AuthError("validation_failed", "Enter account credentials.", 422) from exc
    if not isinstance(body, dict):
        raise AuthError("validation_failed", "Enter account credentials.", 422)
    email, password = body.get("email"), body.get("password")
    if not isinstance(email, str) or not isinstance(password, str):
        raise AuthError("validation_failed", "Enter account credentials.", 422)
    return email, password


def _session_response(settings: Settings, token: str, csrf: str) -> Response:
    response = Response(
        content={"data": {"authenticated": True, "csrfToken": csrf}}, status_code=200
    )
    response.set_cookie(
        key=SESSION_COOKIE,
        value=token,
        httponly=True,
        samesite="lax",
        secure=settings.secure_cookies,
        max_age=settings.session_ttl_seconds,
        path="/",
    )
    return response


@get("/api/v1/auth/csrf")
async def csrf(request: Request[Any, Any, Any]) -> Response:
    return Response(
        content={"data": {"csrfToken": anonymous_csrf_token(_settings(request))}},
        headers={"Cache-Control": "no-store"},
    )


@post("/api/v1/auth/register")
async def register(request: Request[Any, Any, Any]) -> Response:
    settings = _settings(request)
    if not valid_anonymous_csrf(settings, request.headers.get(CSRF_HEADER)):
        return _error_response("csrf_invalid", "A fresh security token is required.", 403)
    try:
        _, token, session_csrf = _service(request).register(*await _credentials(request))
    except AuthError as exc:
        return _error_response(exc.code, exc.message, exc.status_code)
    return _session_response(settings, token, session_csrf)


@post("/api/v1/auth/sign-in")
async def sign_in(request: Request[Any, Any, Any]) -> Response:
    settings = _settings(request)
    if not valid_anonymous_csrf(settings, request.headers.get(CSRF_HEADER)):
        return _error_response("csrf_invalid", "A fresh security token is required.", 403)
    try:
        _, token, session_csrf = _service(request).sign_in(*await _credentials(request))
    except AuthError as exc:
        return _error_response(exc.code, exc.message, exc.status_code)
    return _session_response(settings, token, session_csrf)


@get("/api/v1/auth/session")
async def session(request: Request[Any, Any, Any]) -> Response:
    try:
        actor, _ = _service(request).actor(request.cookies.get(SESSION_COOKIE))
    except AuthError as exc:
        return _error_response(exc.code, exc.message, exc.status_code)
    token = request.cookies.get(SESSION_COOKIE)
    assert token is not None
    return Response(
        content={"data": {"authenticated": True, "csrfToken": _session_csrf(actor, token)}},
        headers={"Cache-Control": "no-store"},
    )


@post("/api/v1/auth/sign-out")
async def sign_out(request: Request[Any, Any, Any]) -> Response:
    token = request.cookies.get(SESSION_COOKIE)
    try:
        actor, _ = _service(request).actor(token)
        if not token or not valid_session_csrf(actor, token, request.headers.get(CSRF_HEADER)):
            return _error_response("csrf_invalid", "A fresh security token is required.", 403)
        _service(request).sign_out(token)
    except AuthError as exc:
        return _error_response(exc.code, exc.message, exc.status_code)
    response = Response(content=None, status_code=HTTP_204_NO_CONTENT)
    response.delete_cookie(SESSION_COOKIE, path="/")
    return response
