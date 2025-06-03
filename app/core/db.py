from sqlmodel import Session, create_engine

from .settings import settings

engine = create_engine(settings.database_url.get_secret_value(), echo=True)


def get_session():
    with Session(engine) as session:
        yield session
