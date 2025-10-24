from fastapi import APIRouter

router = APIRouter()


@router.get("/healthz")
async def health() -> dict:
    return {"status": "ok"}


@router.get("/readyz")
async def ready() -> dict:
    # Could add checks (DB connectivity, external services) here
    return {"ready": True}
