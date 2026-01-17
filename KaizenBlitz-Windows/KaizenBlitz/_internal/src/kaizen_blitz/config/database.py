"""Database configuration and session management."""

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session

from .settings import settings
from ..models.base import Base


# Create engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# Create session factory
session_factory = sessionmaker(bind=engine, autocommit=False, autoflush=False)
SessionLocal = scoped_session(session_factory)


def init_db() -> None:
    """Initialize the database by creating all tables."""
    # Import all models to ensure they are registered with Base
    from ..models import (
        Project,
        FiveWhys,
        IshikawaDiagram,
        IshikawaCategory,
        ActionPlan,
        ActionPlanTask,
    )
    
    # Create all tables
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Get database session.
    
    Yields:
        Database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def close_db() -> None:
    """Close database connections."""
    SessionLocal.remove()
