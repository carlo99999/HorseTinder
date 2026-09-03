"""Owner-scoped Horse Profile persistence and public DTO projection."""

from datetime import UTC, datetime
from typing import Any
from urllib.parse import urlparse
from uuid import UUID

from sqlalchemy import Engine, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.models import HorseProfile


class ProfileError(Exception):
    def __init__(
        self, code: str, message: str, status_code: int, details: dict[str, str] | None = None
    ) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details


PROFILE_FIELDS = ("displayName", "imageUrl", "bio", "trait")


def _utc_timestamp(value: datetime) -> str:
    if value.tzinfo is None:
        value = value.replace(tzinfo=UTC)
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


def profile_dto(profile: HorseProfile) -> dict[str, str]:
    return {
        "id": str(profile.id),
        "displayName": profile.display_name,
        "imageUrl": profile.image_url,
        "bio": profile.bio,
        "trait": profile.trait,
        "createdAt": _utc_timestamp(profile.created_at),
        "updatedAt": _utc_timestamp(profile.updated_at),
    }


def validate_profile(payload: Any) -> dict[str, str]:
    if not isinstance(payload, dict):
        raise ProfileError(
            "validation_failed",
            "Enter your profile details.",
            422,
            {field: "Enter a valid value." for field in PROFILE_FIELDS},
        )
    errors: dict[str, str] = {}
    values: dict[str, str] = {}
    limits = {"displayName": 100, "imageUrl": 500, "bio": 500, "trait": 100}
    labels = {
        "displayName": "Display name",
        "imageUrl": "Image URL",
        "bio": "Bio",
        "trait": "Trait",
    }
    for field in PROFILE_FIELDS:
        value = payload.get(field)
        if not isinstance(value, str) or not value.strip():
            errors[field] = f"{labels[field]} is required."
        elif len(value.strip()) > limits[field]:
            errors[field] = f"{labels[field]} must be {limits[field]} characters or fewer."
        else:
            values[field] = value.strip()
    image_url = values.get("imageUrl")
    if image_url:
        parsed = urlparse(image_url)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            errors["imageUrl"] = "Image URL must include http:// or https:// and a hostname."
    if errors:
        raise ProfileError(
            "validation_failed", "Check the highlighted profile fields.", 422, errors
        )
    return values


class ProfileService:
    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def get(self, account_id: UUID) -> HorseProfile:
        with Session(self.engine) as db:
            profile = db.scalar(select(HorseProfile).where(HorseProfile.account_id == account_id))
            if profile is None:
                raise ProfileError(
                    "profile_not_found", "Set up your Horse Profile to continue.", 404
                )
            db.expunge(profile)
            return profile

    def create(self, account_id: UUID, payload: Any) -> HorseProfile:
        values = validate_profile(payload)
        with Session(self.engine) as db:
            if db.scalar(select(HorseProfile.id).where(HorseProfile.account_id == account_id)):
                raise ProfileError(
                    "profile_exists", "You already have a Horse Profile. Edit it instead.", 409
                )
            if db.scalar(
                select(HorseProfile.id).where(HorseProfile.display_name == values["displayName"])
            ):
                raise ProfileError(
                    "display_name_taken", "That display name is already in the stable.", 409
                )
            profile = HorseProfile(
                account_id=account_id,
                display_name=values["displayName"],
                image_url=values["imageUrl"],
                bio=values["bio"],
                trait=values["trait"],
                created_at=datetime.now(UTC),
                updated_at=datetime.now(UTC),
            )
            db.add(profile)
            try:
                db.commit()
            except IntegrityError as exc:
                db.rollback()
                raise ProfileError(
                    "profile_conflict", "Profile could not be saved. Try again.", 409
                ) from exc
            db.refresh(profile)
            db.expunge(profile)
            return profile

    def update(self, account_id: UUID, payload: Any) -> HorseProfile:
        values = validate_profile(payload)
        with Session(self.engine) as db:
            profile = db.scalar(select(HorseProfile).where(HorseProfile.account_id == account_id))
            if profile is None:
                raise ProfileError(
                    "profile_not_found", "Set up your Horse Profile to continue.", 404
                )
            if db.scalar(
                select(HorseProfile.id).where(
                    HorseProfile.display_name == values["displayName"],
                    HorseProfile.id != profile.id,
                )
            ):
                raise ProfileError(
                    "display_name_taken", "That display name is already in the stable.", 409
                )
            profile.display_name = values["displayName"]
            profile.image_url = values["imageUrl"]
            profile.bio = values["bio"]
            profile.trait = values["trait"]
            profile.updated_at = datetime.now(UTC)
            try:
                db.commit()
            except IntegrityError as exc:
                db.rollback()
                raise ProfileError(
                    "profile_conflict", "That display name is already in the stable.", 409
                ) from exc
            db.refresh(profile)
            db.expunge(profile)
            return profile
