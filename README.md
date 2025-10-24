### Katana Link - FastAPI Starter

A minimal, production-ready FastAPI project scaffold designed to be maintainable, database-friendly, and easy to develop with. It follows a clean modular structure with a repository + service pattern.

Features
- FastAPI with application factory pattern
- Repository + Service pattern for business logic separation
- SQLAlchemy setup (SQLite by default; can be swapped for PostgreSQL)
- Pydantic settings via environment variables
- Health and readiness endpoints
- CORS middleware
- Structured logging
- Auto table creation in development

Project structure
- katana/
  - main.py              — ASGI app entry (used by uvicorn/gunicorn)
  - app.py               — Application factory and lifespan
  - api/
    - __init__.py        — Aggregated API router
    - deps.py            — Dependencies (DB session)
    - routes/
      - health.py        — /healthz and /readyz endpoints
      - users.py         — Example CRUD routes using service layer
  - core/
    - config.py          — Settings (env-based)
    - logging.py         — Logging setup
  - db/
    - session.py         — SQLAlchemy engine + SessionLocal
  - models/
    - base.py            — Declarative Base
    - user.py            — Example User model
  - repositories/
    - user_repository.py — Repository implementing DB operations
  - schemas/
    - user.py            — Pydantic schemas for request/response
  - services/
    - user_service.py    — Business logic using repository

Requirements
- Python 3.11+
- pip or uv/pdm/poetry

Environment variables
- PROJECT_NAME: default "Katana Link"
- VERSION: default "0.1.0"
- ENV: "development" | "production" (default: development)
- ENABLE_DOCS: true/false (default: true)
- LOG_LEVEL: DEBUG/INFO/WARN/ERROR (default: INFO)
- DATABASE_URL: default "sqlite:///./app.db"
- SQL_ECHO: true/false (default: false)

You can copy .env.example to .env and adjust.

Quick start (development)
1. Create a virtual environment and install dependencies:
   - pip install "fastapi>=0.110" "uvicorn[standard]>=0.23" "pydantic>=2.6" "pydantic-settings>=2.2" "SQLAlchemy>=2.0"
2. Optionally create .env from example and tweak values.
3. Run the server:
   - uvicorn katana.main:app --reload
4. Open docs:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

Production
- Use a production ASGI server (gunicorn + uvicorn workers):
  - pip install gunicorn "uvicorn[standard]"
  - gunicorn -k uvicorn.workers.UvicornWorker -w 4 -b 0.0.0.0:8000 katana.main:app
- Prefer a robust DB (e.g., PostgreSQL). Set DATABASE_URL accordingly, e.g.:
  - DATABASE_URL=postgresql+psycopg://user:pass@host:5432/dbname
- Run migrations (Alembic recommended) instead of auto-creating tables in production. The app will not fail if migrations are not present, but you should manage schema via Alembic.

Repository pattern example
- Repositories handle data access (SQLAlchemy session)
- Services implement business logic and orchestrate repositories
- Routers call services and map schemas

Example API usage
- Create user:
  - POST /users
  - Body: { "email": "a@b.com", "full_name": "Alice" }
- List users: GET /users
- Get user: GET /users/{id}
- Update user: PUT /users/{id}
- Delete user: DELETE /users/{id}

Notes
- In development, tables are auto-created on startup for convenience (SQLite default). Switch to a real DB and migrations for production.
- Logging is unified with uvicorn loggers for consistent output.

License
- MIT (customize as needed)
