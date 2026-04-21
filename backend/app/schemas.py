from datetime import datetime
from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    query: str
    platforms: list[str] | None = None


class AnalyzeResponse(BaseModel):
    job_id: int
    status: str


class ChatRequest(BaseModel):
    message: str
    job_id: int | None = None


class ReviewPayload(BaseModel):
    platform: str
    author: str | None = None
    language: str = "en"
    rating: float | None = None
    text: str
    posted_at: datetime | None = None
    source_url: str | None = None
