from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, Text, UniqueConstraint, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import Uuid


class Base(DeclarativeBase):
    pass


class HorseProfile(Base):
    __tablename__ = "horse_profiles"
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    display_name: Mapped[str] = mapped_column(String(100), unique=True)
    image_url: Mapped[str] = mapped_column(String(500))
    bio: Mapped[str] = mapped_column(Text)
    trait: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Match(Base):
    __tablename__ = "matches"
    __table_args__ = (
        UniqueConstraint("first_profile_id", "second_profile_id"),
        CheckConstraint("first_profile_id < second_profile_id", name="matches_canonical_pair"),
    )
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    first_profile_id: Mapped[UUID] = mapped_column(ForeignKey("horse_profiles.id"))
    second_profile_id: Mapped[UUID] = mapped_column(ForeignKey("horse_profiles.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Gesture(Base):
    __tablename__ = "gestures"
    __table_args__ = (
        UniqueConstraint("from_profile_id", "to_profile_id", "kind"),
        CheckConstraint("from_profile_id <> to_profile_id", name="gestures_not_self"),
        CheckConstraint("kind IN ('neigh', 'skip')", name="gestures_kind_valid"),
    )
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    from_profile_id: Mapped[UUID] = mapped_column(ForeignKey("horse_profiles.id"))
    to_profile_id: Mapped[UUID] = mapped_column(ForeignKey("horse_profiles.id"))
    kind: Mapped[str] = mapped_column(String(32))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
