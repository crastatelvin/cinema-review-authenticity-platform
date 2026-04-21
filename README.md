# Cinema Review Authenticity Platform

Production-oriented platform to ingest movie reviews across multiple sources, detect suspicious/fake patterns, and produce an explainable authenticity score.

## Monorepo Structure

- `backend/` FastAPI, Celery, SQLAlchemy, Alembic, ML + scraping pipeline
- `frontend/` Next.js dashboard + chat interface
- `docker-compose.yml` local stack for API, DB, queue, cache

## Quick Start

1. Copy `.env.example` to `.env`.
2. Start services:
   - `docker compose up --build`
3. Open:
   - API docs: `http://localhost:8000/docs`
   - Frontend: `http://localhost:3000`

## Notes

- Some sources should be API-first in production due to scraping restrictions.
- Scraper modules are feature-flagged.
- Scoring is explainable through model outputs and heuristics.
