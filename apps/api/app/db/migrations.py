from sqlalchemy import Engine, create_engine, text

from app.db.models import Base

MIGRATION_VERSION = "0001_foundation"


def make_engine(database_url: str) -> Engine:
    return create_engine(database_url, pool_pre_ping=True)


def migrate(engine: Engine) -> None:
    with engine.begin() as connection:
        connection.execute(
            text("CREATE TABLE IF NOT EXISTS schema_migrations (version VARCHAR(64) PRIMARY KEY)")
        )
        applied = connection.execute(
            text("SELECT 1 FROM schema_migrations WHERE version = :version"),
            {"version": MIGRATION_VERSION},
        ).scalar()
        if not applied:
            Base.metadata.create_all(connection)
            connection.execute(
                text("INSERT INTO schema_migrations (version) VALUES (:version)"),
                {"version": MIGRATION_VERSION},
            )
