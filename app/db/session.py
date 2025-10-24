# Async database session and engine setup for PostgreSQL
from __future__ import annotations

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from ..core.config import get_settings

settings = get_settings()


def _ensure_asyncpg_driver(url: str) -> str:
    """Ensure the database URL uses asyncpg driver for PostgreSQL.

    Converts postgresql:// to postgresql+asyncpg://
    """
    if url.startswith("postgresql://") and not url.startswith("postgresql+asyncpg://"):
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    return url


# Create async engine for PostgreSQL
engine = create_async_engine(
    _ensure_asyncpg_driver(settings.DATABASE_URL),
    echo=settings.SQL_ECHO,
    pool_pre_ping=True,
    pool_size=settings.SQL_POOL_SIZE,
    max_overflow=settings.SQL_MAX_OVERFLOW,
)

# Async session factory
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)