from celery import Celery

from app.core.config import settings
from app.services.analysis_service import run_job

celery_app = Celery(
    "cinema_review",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)


@celery_app.task
def health_ping() -> str:
    return "ok"


@celery_app.task
def run_analysis_job(job_id: int) -> str:
    run_job(job_id)
    return f"processed:{job_id}"
