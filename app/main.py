from app.app import app  # re-export for uvicorn: `uvicorn app.main:app --reload`

__all__ = ["app"]
