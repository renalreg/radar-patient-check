from rr_connection_manager import PostgresConnection

from .config import settings


def get_session():
    if not settings.server:
        raise ValueError("server is not set")

    conn = PostgresConnection(
        app=settings.server,
        tunnel=settings.with_tunnel,
        via_app=settings.via_app,
    )
    ukrdc_sessionmaker = conn.session_maker(autocommit=False, autoflush=False)

    db = ukrdc_sessionmaker()
    try:
        yield db
    finally:
        db.close()
