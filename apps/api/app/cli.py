from app.config import Settings
from app.db.fixtures import load_fixtures
from app.db.migrations import make_engine, migrate


def prepare_database() -> None:
    settings = Settings.from_environment()
    engine = make_engine(settings.database_url)
    migrate(engine)
    load_fixtures(engine)


if __name__ == "__main__":
    prepare_database()
