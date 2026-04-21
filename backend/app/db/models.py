from datetime import datetime
from enum import Enum

from pgvector.sqlalchemy import Vector
from sqlalchemy import JSON, DateTime, Enum as SAEnum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Platform(str, Enum):
    generic_web = "generic_web"
    imdb = "imdb"
    rotten_tomatoes = "rotten_tomatoes"
    metacritic = "metacritic"
    letterboxd = "letterboxd"
    tmdb = "tmdb"
    omdb = "omdb"
    reddit = "reddit"
    bookmyshow = "bookmyshow"
    koimoi = "koimoi"
    bollywood_hungama = "bollywood_hungama"
    times_of_india = "times_of_india"


class JobStatus(str, Enum):
    queued = "queued"
    running = "running"
    completed = "completed"
    failed = "failed"


class Movie(Base):
    __tablename__ = "movies"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(256), index=True)
    year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    reviews = relationship("Review", back_populates="movie")


class Review(Base):
    __tablename__ = "reviews"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), index=True)
    platform: Mapped[Platform] = mapped_column(SAEnum(Platform), index=True)
    source_url: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    author: Mapped[str | None] = mapped_column(String(256), nullable=True)
    language: Mapped[str] = mapped_column(String(16), default="en")
    rating: Mapped[float | None] = mapped_column(Float, nullable=True)
    text: Mapped[str] = mapped_column(Text)
    posted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    fake_probability: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    movie = relationship("Movie", back_populates="reviews")
    embedding = relationship("ReviewEmbedding", uselist=False, back_populates="review")


class ReviewEmbedding(Base):
    __tablename__ = "review_embeddings"
    review_id: Mapped[int] = mapped_column(ForeignKey("reviews.id"), primary_key=True)
    embedding: Mapped[list[float]] = mapped_column(Vector(384))
    review = relationship("Review", back_populates="embedding")


class AnalysisJob(Base):
    __tablename__ = "analysis_jobs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    query: Mapped[str] = mapped_column(String(512))
    status: Mapped[JobStatus] = mapped_column(SAEnum(JobStatus), default=JobStatus.queued)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    result: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class PlatformReport(Base):
    __tablename__ = "platform_reports"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("analysis_jobs.id"), index=True)
    platform: Mapped[Platform] = mapped_column(SAEnum(Platform), index=True)
    score: Mapped[float] = mapped_column(Float)
    details: Mapped[dict] = mapped_column(JSON)
