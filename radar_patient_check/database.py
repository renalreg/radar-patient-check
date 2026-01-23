from rr_connection_manager import PostgresConnection
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import settings


def get_session():
    if settings.database_url:
        engine = create_engine(url=settings.database_url)
        ukrdc_sessionmaker = sessionmaker(
            bind=engine, autoflush=False, autocommit=False
        )
        db = ukrdc_sessionmaker()
    else:
        if not settings.SERVER:
            raise ValueError("SERVER is not set")

        conn = PostgresConnection(
            app=settings.SERVER,
            tunnel=settings.WITH_TUNNEL,
            via_app=settings.VIA_APP,
        )
        ukrdc_sessionmaker = conn.session_maker(autocommit=False, autoflush=False)

        db = ukrdc_sessionmaker()
    try:
        yield db
    finally:
        db.close()
