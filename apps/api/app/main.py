import json
import logging
from typing import Any

from litestar import Litestar, Request, Response, get
from litestar.exceptions import HTTPException, NotFoundException
from litestar.status_codes import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

from app.config import ConfigurationError, Settings
from app.db.migrations import make_engine, migrate

logger = logging.getLogger("horsetinder.api")


def error_response(
    code: str, message: str, status_code: int, details: dict[str, Any] | None = None
) -> Response:
    body: dict[str, Any] = {"code": code, "message": message}
    if details:
        body["details"] = details
    return Response(content=body, status_code=status_code)


@get("/api/v1/health")
async def health() -> dict[str, dict[str, str]]:
    return {"data": {"service": "horse-tinder-api", "version": "v1"}}


class RequestLoggingMiddleware:
    """Emit JSON request events without leaking request bodies or secrets."""

    def __init__(self, app: Any) -> None:
        self.app = app

    async def __call__(self, scope: dict[str, Any], receive: Any, send: Any) -> None:
        status_code = 500

        async def log_response(message: dict[str, Any]) -> None:
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = message["status"]
            await send(message)

        try:
            await self.app(scope, receive, log_response)
        except Exception:
            logger.exception(json.dumps({"event": "request_error", "path": scope.get("path")}))
            raise
        logger.info(
            json.dumps(
                {
                    "event": "request",
                    "method": scope.get("method"),
                    "path": scope.get("path"),
                    "status": status_code,
                }
            )
        )


def exception_handler(_: Request[Any, Any, Any], exc: Exception) -> Response:
    if isinstance(exc, NotFoundException | HTTPException):
        return error_response("not_found", "API route was not found.", HTTP_404_NOT_FOUND)
    logger.exception(json.dumps({"event": "unhandled_error", "type": type(exc).__name__}))
    return error_response(
        "internal_error", "An unexpected server error occurred.", HTTP_500_INTERNAL_SERVER_ERROR
    )


def create_app(settings: Settings | None = None, *, run_migrations: bool = True) -> Litestar:
    try:
        settings = settings or Settings.from_environment()
    except ConfigurationError as exc:
        logger.error(
            json.dumps(
                {
                    "event": "startup_failure",
                    "code": "configuration_invalid",
                    "message": str(exc),
                }
            )
        )
        raise
    if run_migrations:
        try:
            migrate(make_engine(settings.database_url))
        except Exception:
            logger.exception(json.dumps({"event": "startup_failure", "code": "migration_failed"}))
            raise
    return Litestar(
        route_handlers=[health],
        middleware=[RequestLoggingMiddleware],
        exception_handlers={Exception: exception_handler},
        openapi_config=None,
    )
