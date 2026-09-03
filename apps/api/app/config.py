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

    @classmethod
    def from_environment(cls) -> "Settings":
        missing = [name for name in ("DATABASE_URL", "APP_SECRET") if not os.getenv(name)]
        if missing:
            raise ConfigurationError(f"Missing required API configuration: {', '.join(missing)}")
        return cls(
            os.environ["DATABASE_URL"],
            os.environ["APP_SECRET"],
            os.getenv("APP_ENV", "development"),
        )
