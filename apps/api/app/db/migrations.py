from importlib import import_module
from typing import Protocol, cast

from sqlalchemy import Connection, Engine, create_engine, text


class Migration(Protocol):
    revision: str

    def upgrade(self, connection: Connection) -> None: ...


MIGRATION_MODULES = ("app.db.migration_versions.foundation_0001",)


def migrations() -> tuple[Migration, ...]:
    """Return ordered, independently applicable revisions for deterministic upgrades."""
    loaded = tuple(import_module(module) for module in MIGRATION_MODULES)
    return tuple(
        sorted(
            (cast(Migration, migration) for migration in loaded),
            key=lambda migration: migration.revision,
        )
    )


def make_engine(database_url: str) -> Engine:
    return create_engine(database_url, pool_pre_ping=True)


def migrate(engine: Engine) -> None:
    with engine.begin() as connection:
        if engine.dialect.name == "postgresql":
            connection.execute(text("SELECT pg_advisory_xact_lock(813_401_001)"))
        connection.execute(
            text("CREATE TABLE IF NOT EXISTS schema_migrations (version VARCHAR(64) PRIMARY KEY)")
        )
        applied = set(connection.execute(text("SELECT version FROM schema_migrations")).scalars())
        for migration in migrations():
            if migration.revision in applied:
                continue
            migration.upgrade(connection)
            connection.execute(
                text("INSERT INTO schema_migrations (version) VALUES (:version)"),
                {"version": migration.revision},
            )
