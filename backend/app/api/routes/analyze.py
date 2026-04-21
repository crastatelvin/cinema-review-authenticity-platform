from fastapi import APIRouter

from app.db.models import AnalysisJob
from app.db.session import SessionLocal
from app.schemas import AnalyzeRequest, AnalyzeResponse
from app.services.analysis_service import create_job
from app.tasks.celery_app import run_analysis_job

router = APIRouter(prefix="/api", tags=["analyze"])


@router.post("/analyze", response_model=AnalyzeResponse)
def enqueue_analysis(payload: AnalyzeRequest):
    job_id = create_job(payload.query)
    run_analysis_job.delay(job_id)
    return AnalyzeResponse(job_id=job_id, status="queued")


@router.get("/analyze/{job_id}")
def get_analysis(job_id: int):
    with SessionLocal() as db:
        job = db.get(AnalysisJob, job_id)
        if job is None:
            return {"status": "not_found"}
        return {
            "job_id": job.id,
            "query": job.query,
            "status": job.status.value if hasattr(job.status, "value") else str(job.status),
            "result": job.result,
            "error_message": job.error_message,
        }
