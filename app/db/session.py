# Async database session and engine setup (SQLite or PostgreSQL)
from __future__ import annotations

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import get_settings

settings = get_settings()


def _normalize_db_url(url: str) -> str:
    """Normalize database URL for async drivers.

    - For PostgreSQL, ensure asyncpg driver is used.
    - Leave SQLite urls as-is (e.g., sqlite+aiosqlite:///./app.db).
    """
    if url.startswith("postgresql://") and not url.startswith("postgresql+asyncpg://"):
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    return url


url = _normalize_db_url(settings.DATABASE_URL)

# Engine args adjusted for SQLite vs others
engine_kwargs = dict(echo=settings.SQL_ECHO, pool_pre_ping=True)
if url.startswith("sqlite+"):
    # SQLite async driver manages its own pooling; avoid pool_size/max_overflow
    pass
else:
    engine_kwargs.update(pool_size=settings.SQL_POOL_SIZE, max_overflow=settings.SQL_MAX_OVERFLOW)

# Create async engine
engine = create_async_engine(url, **engine_kwargs)

# Async session factory
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)