"""Server-only configuration validation."""

import os
from dataclasses import dataclass


class ConfigurationError(RuntimeError):
    """Raised before traffic is accepted when a required setting is absent."""


@dataclass(frozen=True)
class Settings:
    database_url: str
    app_secret: str
    environment: str = "development"
    session_ttl_seconds: int = 60 * 60 * 24 * 14

    @property
    def secure_cookies(self) -> bool:
        return self.environment.lower() == "production"

    @classmethod
    def from_environment(cls) -> "Settings":
        missing = [name for name in ("DATABASE_URL", "APP_SECRET") if not os.getenv(name)]
        if missing:
            raise ConfigurationError(f"Missing required API configuration: {', '.join(missing)}")
        ttl = int(os.getenv("SESSION_TTL_SECONDS", str(60 * 60 * 24 * 14)))
        if ttl <= 0:
            raise ConfigurationError("SESSION_TTL_SECONDS must be a positive integer")
        return cls(
            os.environ["DATABASE_URL"],
            os.environ["APP_SECRET"],
            os.getenv("APP_ENV", "development"),
            ttl,
        )
