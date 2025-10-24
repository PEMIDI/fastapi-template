from app.api.routes.health import router as health_router  # re-export

from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(health_router, tags=["health"])
