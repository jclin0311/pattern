from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from ..config import settings


class Base(DeclarativeBase):
    pass


def sqlalchemy_url(url: str) -> str:
    """Hosts such as Neon hand out plain postgres:// URLs; route them through psycopg 3."""
    for scheme in ("postgres://", "postgresql://"):
        if url.startswith(scheme):
            return "postgresql+psycopg://" + url.removeprefix(scheme)
    return url


def make_engine(url: str):
    url = sqlalchemy_url(url)
    if url.startswith("sqlite"):
        return create_engine(url, pool_pre_ping=True, connect_args={"check_same_thread": False})
    # Sized for one uvicorn worker: keep the host's concurrency (Cloud Run --concurrency 20)
    # near pool_size + max_overflow, and the total across instances under max_connections.
    # These options need a direct connection; Neon's -pooler endpoint rejects `options`.
    return create_engine(
        url,
        pool_size=5,
        max_overflow=10,
        pool_timeout=10,  # fail fast when every connection is busy
        pool_recycle=300,  # serverless Postgres drops idle connections when it scales to zero
        pool_pre_ping=True,
        connect_args={
            "connect_timeout": 10,  # allows for a suspended compute waking up
            "options": "-c statement_timeout=15000",
        },
    )


engine = make_engine(settings.database_url)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
