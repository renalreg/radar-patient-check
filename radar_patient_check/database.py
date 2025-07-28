from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import settings

_engine = None


def get_session():
    global _engine

    if not settings.sqlalchemy_database_url:
        raise ValueError("SQLALCHEMY_DATABASE_URL not set")

    if _engine is None:
        _engine = create_engine(settings.sqlalchemy_database_url)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
