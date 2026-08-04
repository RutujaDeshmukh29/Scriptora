"""
Database engine and session factory.

Uses sync SQLAlchemy deliberately for V1: the real-time collaboration workload
(the part that actually needs an async/event-driven runtime) lives in the
separate Hocuspocus service, not here. This API is mostly REST CRUD, where a
sync engine is simpler to reason about, simpler to debug, and one less moving
part while shipping the 3-day sprint. Revisit only if profiling shows the sync
DB layer is actually the bottleneck.
"""
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True, pool_recycle=200, future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency — yields a request-scoped DB session and always closes it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
