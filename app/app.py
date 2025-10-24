from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import get_settings
from .core.logging import setup_logging
from .api.routes import api_router
from .db.session import engine
from .models.base import Base

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context.

    - On startup: configure logging and, in non-production, create DB tables automatically.
    - On shutdown: dispose DB engine.
    """
    settings = get_settings()
    setup_logging(level=settings.LOG_LEVEL)

    # Auto-create tables outside production for convenience
    if settings.ENV.lower() != "production":
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables ensured (create_all) for environment=%s", settings.ENV)
        except Exception as exc:
            logger.exception("Failed to auto-create tables on startup: %s", exc)

    # Yield control to the application runtime
    yield

    # Shutdown: close connections, flush metrics, etc.
    try:
        await engine.dispose()
    except Exception as exc:
        logger.warning("Error during engine.dispose(): %s", exc)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    settings = get_settings()

    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        docs_url="/docs" if settings.ENABLE_DOCS else None,
        redoc_url="/redoc" if settings.ENABLE_DOCS else None,
        openapi_url="/openapi.json" if settings.ENABLE_DOCS else None,
        lifespan=lifespan,
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers
    app.include_router(api_router)

    return app


# Create the app instance at module level
app = create_app()