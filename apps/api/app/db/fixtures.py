from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

from app.db.models import Gesture, HorseProfile, Match

FIXTURE_PROFILES = (
    (
        "Clover Comet",
        "https://example.invalid/clover.jpg",
        "Night gallops and oat-milk lattes.",
        "Stargazer",
    ),
    (
        "Juniper Jumps",
        "https://example.invalid/juniper.jpg",
        "Looking for a steady trot and silly puns.",
        "Trailblazer",
    ),
)


def load_fixtures(engine: Engine) -> None:
    with Session(engine) as session, session.begin():
        profiles: dict[str, HorseProfile] = {}
        for name, image_url, bio, trait in FIXTURE_PROFILES:
            profile = session.scalar(select(HorseProfile).where(HorseProfile.display_name == name))
            if profile is None:
                profile = HorseProfile(display_name=name, image_url=image_url, bio=bio, trait=trait)
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
            session.add(Match(first_profile_id=clover.id, second_profile_id=juniper.id))
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
                    Gesture(from_profile_id=source.id, to_profile_id=destination.id, kind="neigh")
                )
