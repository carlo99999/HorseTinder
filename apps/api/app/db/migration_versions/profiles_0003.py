"""Add optional profile ownership without changing deterministic fixture identities."""

from sqlalchemy import (
    Column,
    Connection,
    DateTime,
    ForeignKeyConstraint,
    Index,
    MetaData,
    Table,
    text,
)
from sqlalchemy.schema import AddConstraint, CreateColumn
from sqlalchemy.types import Uuid

revision = "0003_profiles"


def upgrade(connection: Connection) -> None:
    """Make account ownership durable while retaining unowned existing fixtures."""
    columns = {
        column["name"] for column in connection.dialect.get_columns(connection, "horse_profiles")
    }
    if "account_id" not in columns:
        account_id = Column("account_id", Uuid, nullable=True)
        definition = CreateColumn(account_id).compile(connection.dialect)
        connection.execute(text(f"ALTER TABLE horse_profiles ADD COLUMN {definition}"))
    if "updated_at" not in columns:
        updated_at = Column(
            "updated_at",
            DateTime(timezone=True),
            server_default=text("CURRENT_TIMESTAMP"),
            nullable=False,
        )
        definition = CreateColumn(updated_at).compile(connection.dialect)
        connection.execute(text(f"ALTER TABLE horse_profiles ADD COLUMN {definition}"))
    profiles = Table("horse_profiles", MetaData(), autoload_with=connection)
    if connection.dialect.name == "postgresql":
        foreign_key = ForeignKeyConstraint(
            [profiles.c.account_id], ["accounts.id"], name="horse_profiles_account_id_fkey"
        )
        if "horse_profiles_account_id_fkey" not in {
            constraint["name"]
            for constraint in connection.dialect.get_foreign_keys(connection, "horse_profiles")
        }:
            connection.execute(AddConstraint(foreign_key))
    # A partial unique index permits any number of fixture profiles while enforcing one
    # profile for each real account in both PostgreSQL and the SQLite test database.
    index = Index(
        "horse_profiles_one_profile_per_account",
        profiles.c.account_id,
        unique=True,
        postgresql_where=profiles.c.account_id.is_not(None),
        sqlite_where=profiles.c.account_id.is_not(None),
    )
    index.create(connection, checkfirst=True)
