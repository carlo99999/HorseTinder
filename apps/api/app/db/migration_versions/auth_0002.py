"""Create durable account and revocable session persistence."""

from typing import cast

from sqlalchemy import Connection, Table

from app.db.models import Account, AccountSession

revision = "0002_auth"


def upgrade(connection: Connection) -> None:
    for model in (Account, AccountSession):
        cast(Table, model.__table__).create(connection, checkfirst=True)
