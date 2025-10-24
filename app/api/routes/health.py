from fastapi import APIRouter
from app.core.config import get_settings
from app.db.session import AsyncSessionLocal

router = APIRouter()


@router.get("/healthz")
async def health() -> dict:
    settings = get_settings()
    return {"status": "ok", "version": settings.VERSION, "env": settings.ENV}


@router.get("/readyz")
async def ready() -> dict:
    settings = get_settings()
    db_ok = True
    try:
        # Simple DB connectivity check
        async with AsyncSessionLocal() as session:
            await session.execute("SELECT 1")
    except Exception:
        db_ok = False
    return {"ready": db_ok, "db": db_ok, "version": settings.VERSION, "env": settings.ENV}
