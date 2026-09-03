from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

from app.db.models import Gesture, HorseProfile, Match

FIXTURE_PROFILES = (
    (
        UUID("11111111-1111-4111-8111-111111111111"),
        "Clover Comet",
        "https://example.invalid/clover.jpg",
        "Night gallops and oat-milk lattes.",
        "Stargazer",
    ),
    (
        UUID("22222222-2222-4222-8222-222222222222"),
        "Juniper Jumps",
        "https://example.invalid/juniper.jpg",
        "Looking for a steady trot and silly puns.",
        "Trailblazer",
    ),
)
FIXTURE_MATCH_ID = UUID("33333333-3333-4333-8333-333333333333")
FIXTURE_GESTURE_IDS = {
    ("Clover Comet", "Juniper Jumps"): UUID("44444444-4444-4444-8444-444444444444"),
    ("Juniper Jumps", "Clover Comet"): UUID("55555555-5555-4555-8555-555555555555"),
}
FIXTURE_TIMESTAMP = datetime(2026, 1, 1, tzinfo=UTC)


def load_fixtures(engine: Engine) -> None:
    with Session(engine) as session, session.begin():
        profiles: dict[str, HorseProfile] = {}
        for profile_id, name, image_url, bio, trait in FIXTURE_PROFILES:
            profile = session.scalar(select(HorseProfile).where(HorseProfile.display_name == name))
            if profile is None:
                profile = HorseProfile(
                    id=profile_id,
                    display_name=name,
                    image_url=image_url,
                    bio=bio,
                    trait=trait,
                    created_at=FIXTURE_TIMESTAMP,
                )
                session.add(profile)
                session.flush()
            profiles[name] = profile
        clover, juniper = profiles["Clover Comet"], profiles["Juniper Jumps"]
        match = session.scalar(
            select(Match).where(
                Match.first_profile_id == clover.id, Match.second_profile_id == juniper.id
            )
        )
        if match is None:
            session.add(
                Match(
                    id=FIXTURE_MATCH_ID,
                    first_profile_id=clover.id,
                    second_profile_id=juniper.id,
                    created_at=FIXTURE_TIMESTAMP,
                )
            )
        for source, destination in ((clover, juniper), (juniper, clover)):
            existing = session.scalar(
                select(Gesture).where(
                    Gesture.from_profile_id == source.id,
                    Gesture.to_profile_id == destination.id,
                    Gesture.kind == "neigh",
                )
            )
            if existing is None:
                session.add(
                    Gesture(
                        id=FIXTURE_GESTURE_IDS[(source.display_name, destination.display_name)],
                        from_profile_id=source.id,
                        to_profile_id=destination.id,
                        kind="neigh",
                        created_at=FIXTURE_TIMESTAMP,
                    )
                )
