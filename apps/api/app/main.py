import json
import logging
from typing import Any, cast

from litestar import Litestar, Request, Response, get
from litestar.exceptions import HTTPException, NotFoundException
from litestar.middleware import DefineMiddleware
from litestar.status_codes import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

from app.auth.routes import csrf, register, session, sign_in, sign_out
from app.config import ConfigurationError, Settings
from app.db.fixtures import load_fixtures
from app.db.migrations import make_engine, migrate

logger = logging.getLogger("horsetinder.api")


class JsonFormatter(logging.Formatter):
    """Render application events as one structured JSON object per line."""

    def format(self, record: logging.LogRecord) -> str:
        event: dict[str, Any] = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%SZ"),
            "level": record.levelname.lower(),
            "logger": record.name,
        }
        try:
            event.update(json.loads(record.getMessage()))
        except (TypeError, json.JSONDecodeError):
            event["message"] = record.getMessage()
        return json.dumps(event, sort_keys=True)


def configure_logging() -> None:
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False


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
    if isinstance(exc, NotFoundException):
        return error_response("not_found", "API route was not found.", HTTP_404_NOT_FOUND)
    if isinstance(exc, HTTPException):
        detail = exc.detail if isinstance(exc.detail, dict) else None
        message = (
            exc.detail if isinstance(exc.detail, str) else "The request could not be completed."
        )
        return error_response("http_error", message, exc.status_code, detail)
    logger.exception(json.dumps({"event": "unhandled_error", "type": type(exc).__name__}))
    return error_response(
        "internal_error", "An unexpected server error occurred.", HTTP_500_INTERNAL_SERVER_ERROR
    )


def create_app(settings: Settings | None = None, *, run_migrations: bool = True) -> Litestar:
    configure_logging()
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
    engine = make_engine(settings.database_url)
    if run_migrations:
        try:
            migrate(engine)
            load_fixtures(engine)
        except Exception:
            logger.exception(
                json.dumps({"event": "startup_failure", "code": "database_prepare_failed"})
            )
            raise
    app = Litestar(
        route_handlers=[health, csrf, register, sign_in, session, sign_out],
        middleware=[DefineMiddleware(cast(Any, RequestLoggingMiddleware))],
        exception_handlers={Exception: exception_handler},
        openapi_config=None,
    )
    app.state.settings = settings
    app.state.auth_engine = engine
    return app
