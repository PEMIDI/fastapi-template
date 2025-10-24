# Makefile for common development tasks

PY=python3
UVICORN=uvicorn

.PHONY: help install run dev docker-build docker-run migrate revision fmt

help:
	@echo "Available targets:"
	@echo "  install       Install dependencies from requirements.txt"
	@echo "  run           Run the API (production-style)"
	@echo "  dev           Run the API with reload"
	@echo "  docker-build  Build docker image"
	@echo "  docker-run    Run docker container"
	@echo "  migrate       Run Alembic migrations"
	@echo "  revision      Create Alembic revision"
	@echo "  fmt           Format code with ruff/black if installed"

install:
	$(PY) -m pip install -r requirements.txt

run:
	$(UVICORN) app.main:app --host 0.0.0.0 --port 8000

dev:
	$(UVICORN) app.main:app --reload --host 0.0.0.0 --port 8000

docker-build:
	docker build -t fastapi-template:latest .

docker-run:
	docker run --rm -p 8000:8000 --env-file .env fastapi-template:latest

migrate:
	cd app && alembic upgrade head

revision:
	cd app && alembic revision --autogenerate -m "update"

fmt:
	-ruff check --fix . || true
	-black . || true
