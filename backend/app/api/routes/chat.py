from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.agents.chat_agent import chat_reply
from app.db.models import AnalysisJob
from app.db.session import SessionLocal
from app.schemas import ChatRequest

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat")
def chat(payload: ChatRequest):
    analysis = None
    if payload.job_id:
        with SessionLocal() as db:
            job = db.get(AnalysisJob, payload.job_id)
            analysis = job.result if job and job.result else None
    text = chat_reply(payload.message, analysis=analysis)

    async def event_stream():
        for token in text.split():
            yield f"data: {token} \n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
