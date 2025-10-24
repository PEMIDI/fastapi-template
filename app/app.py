from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException
from starlette.responses import JSONResponse
import uuid

from app.core.config import get_settings
from app.core.logging import setup_logging
from app.api.routes import api_router
from app.db.session import engine
from app.models.base import Base

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
        expose_headers=["X-Request-ID"],
    )

    # Error handlers
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        req_id = getattr(request.state, "request_id", None)
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "message": exc.detail,
                    "code": exc.status_code,
                },
                "request_id": req_id,
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        req_id = getattr(request.state, "request_id", None)
        return JSONResponse(
            status_code=422,
            content={
                "error": {
                    "message": "Validation error",
                    "details": exc.errors(),
                    "code": 422,
                },
                "request_id": req_id,
            },
        )

    # Root route
    @app.get("/")
    async def root(request: Request):
        settings = get_settings()
        return {
            "name": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "env": settings.ENV,
            "docs": app.docs_url,
            "redoc": app.redoc_url,
            "openapi": app.openapi_url,
            "health": "/healthz",
            "ready": "/readyz",
            "request_id": request.headers.get("X-Request-ID") or request.state.request_id,
        }

    # Routers
    app.include_router(api_router)

    return app


def request_id_middleware(app: FastAPI):
    @app.middleware("http")
    async def add_request_id(request: Request, call_next):
        req_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        request.state.request_id = req_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = req_id
        return response


# Create the app instance at module level
app = create_app()
request_id_middleware(app)