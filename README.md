## Don't use this repo until the development is finished.

### FastAPI Template Starter

A minimal, production-ready FastAPI project scaffold designed to be maintainable, database-friendly, and easy to develop with. It follows a clean modular structure with a repository + service pattern.

Features
- FastAPI with application factory pattern
- Repository + Service pattern for business logic separation
- SQLAlchemy setup (SQLite by default; can be swapped for PostgreSQL)
- Environment-driven settings with .env support
- Health and readiness endpoints (with DB check)
- Root endpoint with metadata
- CORS middleware
- Structured logging with unified uvicorn output
- Request ID middleware (X-Request-ID)
- Auto table creation in development
- Dockerfile, .dockerignore, Makefile

Project structure
- app/
  - main.py              — ASGI app entry (used by uvicorn/gunicorn)
  - app.py               — Application factory and lifespan
  - api/
    - __init__.py        — Aggregated API router
    - deps.py            — Dependencies (DB session)
    - routes/
      - health.py        — /healthz and /readyz endpoints
  - core/
    - config.py          — Settings (env-based)
    - logging.py         — Logging setup
  - db/
    - session.py         — SQLAlchemy engine + AsyncSessionLocal
  - models/
    - base.py            — Declarative Base
  - repositories/
    - user_repository.py — Example repository (sync style, for reference)
  - services/
    - user_service.py    — Example service (sync style, for reference)

Requirements
- Python 3.11+
- pip (or uv/pdm/poetry)

Environment variables
- PROJECT_NAME: default "FastAPI Template"
- VERSION: default "0.1.0"
- ENV: "development" | "production" (default: development)
- ENABLE_DOCS: true/false (default: true)
- LOG_LEVEL: DEBUG/INFO/WARNING/ERROR (default: INFO)
- DATABASE_URL: default "sqlite+aiosqlite:///./app.db" (use async drivers)
- SQL_ECHO: true/false (default: false)

You can copy .env.example to .env and adjust.

Quick start (development)
1. Create a virtual environment and install dependencies:
   - make install  # or: pip install -r requirements.txt
2. (Optional) Copy .env.example to .env and tweak values.
3. Run the server:
   - make dev  # or: uvicorn app.main:app --reload
4. Open docs:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

Docker
- Build image: make docker-build
- Run container: make docker-run

Production
- Use a production ASGI server (gunicorn + uvicorn workers):
  - pip install gunicorn "uvicorn[standard]"
  - gunicorn -k uvicorn.workers.UvicornWorker -w 4 -b 0.0.0.0:8000 app.main:app
- Prefer a robust DB (e.g., PostgreSQL). Set DATABASE_URL accordingly, e.g.:
  - DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/dbname
- Run migrations (Alembic recommended). In development, tables are auto-created for convenience; in production manage schema with Alembic.

Notes
- Root endpoint (/) returns service metadata and links.
- Health endpoints: /healthz (basic), /readyz (includes DB check).
- Request IDs are returned via X-Request-ID header for tracing.
- Logging is unified with uvicorn for consistent output.

License
- MIT (customize as needed)
