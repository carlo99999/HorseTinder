"""Create the original Horse Tinder persistence schema."""

from typing import cast

from sqlalchemy import Connection, Table

from app.db.models import Gesture, HorseProfile, Match

revision = "0001_foundation"


def upgrade(connection: Connection) -> None:
    """Apply this revision only; later revisions are ordered by their revision key."""
    for model in (HorseProfile, Match, Gesture):
        cast(Table, model.__table__).create(connection, checkfirst=True)
