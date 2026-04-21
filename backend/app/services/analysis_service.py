from __future__ import annotations

import asyncio
from datetime import datetime

from app.agents.report_composer import compose_report
from app.db.models import (
    AnalysisJob,
    JobStatus,
    Movie,
    Platform,
    PlatformReport,
    Review,
    ReviewEmbedding,
)
from app.db.session import SessionLocal
from app.db.vector_store import encode_texts
from app.ml.aggregator import final_authenticity_score, platform_score
from app.ml.duplicate import duplicate_fraction
from app.ml.fake_detector import predict_fake_probability
from app.ml.heuristics import burstiness_index, template_repetition_rate
from app.ml.multilingual import detect_language, multilingual_fake_adjustment
from app.ml.sentiment import rating_sentiment_mismatch, sentiment_score
from app.scrapers.api_sources import OMDBSource, RedditSource, TMDBSource
from app.scrapers.scraped_sources import (
    BookMyShowSource,
    BollywoodHungamaSource,
    GenericReviewPageSource,
    IMDBSource,
    KoimoiSource,
    LetterboxdSource,
    MetacriticSource,
    RottenTomatoesSource,
    TimesOfIndiaSource,
)


def analyze_reviews(raw_reviews: list[dict]) -> dict:
    by_platform: dict[str, list[dict]] = {}
    for row in raw_reviews:
        by_platform.setdefault(row["platform"], []).append(row)

    reports = []
    scores = []
    for platform, reviews in by_platform.items():
        texts = [r["text"] for r in reviews]
        fake_probs = [predict_fake_probability(t) for t in texts]
        sentiments = [sentiment_score(t) for t in texts]
        mismatches = [
            rating_sentiment_mismatch(r.get("rating"), sentiments[i]) for i, r in enumerate(reviews)
        ]
        sc = platform_score(
            f=sum(fake_probs) / max(1, len(fake_probs)),
            d=duplicate_fraction(texts),
            b=burstiness_index([r.get("posted_at") for r in reviews]),
            m=sum(mismatches) / max(1, len(mismatches)),
            t=template_repetition_rate(texts),
        )
        reports.append({"platform": platform, "score": sc * 100, "review_count": len(reviews)})
        scores.append(sc)

    final_score = final_authenticity_score(scores)
    result = {"authenticity_score": final_score, "platforms": reports}
    result["summary"] = compose_report(result)
    return result


async def collect_reviews(query: str) -> list[dict]:
    sources = [TMDBSource(), RedditSource(), OMDBSource()]
    if query.startswith("http"):
        sources.extend(
            [
                GenericReviewPageSource(),
                IMDBSource(),
                RottenTomatoesSource(),
                MetacriticSource(),
                LetterboxdSource(),
                BookMyShowSource(),
                KoimoiSource(),
                BollywoodHungamaSource(),
                TimesOfIndiaSource(),
            ]
        )
    tasks = [source.fetch_reviews(query) for source in sources]
    chunks = await asyncio.gather(*tasks, return_exceptions=False)
    rows: list[dict] = []
    for source_reviews in chunks:
        for rv in source_reviews:
            rows.append(
                {
                    "platform": rv.platform,
                    "text": rv.text,
                    "rating": rv.rating,
                    "author": rv.author,
                    "language": rv.language or detect_language(rv.text),
                    "posted_at": rv.posted_at,
                    "source_url": rv.source_url,
                }
            )
    return rows


def create_job(query: str) -> int:
    with SessionLocal() as db:
        job = AnalysisJob(query=query, status=JobStatus.queued)
        db.add(job)
        db.commit()
        db.refresh(job)
        return job.id


def run_job(job_id: int):
    with SessionLocal() as db:
        job = db.get(AnalysisJob, job_id)
        if job is None:
            return
        job.status = JobStatus.running
        db.commit()

        try:
            raw_reviews = asyncio.run(collect_reviews(job.query))
            if not raw_reviews:
                raise ValueError("No reviews fetched from configured sources for the provided query.")
            analysis = analyze_reviews(raw_reviews)

            movie = Movie(title=job.query, created_at=datetime.utcnow())
            db.add(movie)
            db.flush()

            texts = [r["text"] for r in raw_reviews]
            embeddings = encode_texts(texts)
            for idx, row in enumerate(raw_reviews):
                review = Review(
                    movie_id=movie.id,
                    platform=Platform(row["platform"]),
                    source_url=row.get("source_url"),
                    author=row.get("author"),
                    language=row.get("language") or "en",
                    rating=row.get("rating"),
                    text=row["text"],
                    posted_at=row.get("posted_at"),
                    fake_probability=predict_fake_probability(row["text"])
                    * multilingual_fake_adjustment(row.get("language") or "en"),
                )
                db.add(review)
                db.flush()
                if idx < len(embeddings):
                    db.add(ReviewEmbedding(review_id=review.id, embedding=embeddings[idx]))

            for p in analysis["platforms"]:
                db.add(
                    PlatformReport(
                        job_id=job.id,
                        platform=Platform(p["platform"]),
                        score=p["score"],
                        details={"review_count": p["review_count"]},
                    )
                )

            job.status = JobStatus.completed
            job.result = analysis
            job.updated_at = datetime.utcnow()
            db.commit()
        except Exception as exc:
            job.status = JobStatus.failed
            job.error_message = str(exc)
            job.updated_at = datetime.utcnow()
            db.commit()
