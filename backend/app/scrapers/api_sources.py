from __future__ import annotations

import asyncpraw
import httpx

from app.core.config import settings
from app.scrapers.base import BaseReviewSource, NormalizedReview


class TMDBSource(BaseReviewSource):
    platform = "tmdb"

    async def _search_movie_id(self, query: str) -> int | None:
        url = "https://api.themoviedb.org/3/search/movie"
        params = {"api_key": settings.tmdb_api_key, "query": query}
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
        results = data.get("results", [])
        if not results:
            return None
        return results[0]["id"]

    async def fetch_reviews(self, query: str) -> list[NormalizedReview]:
        if not settings.tmdb_api_key:
            return []
        movie_id = await self._search_movie_id(query)
        if movie_id is None:
            return []
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews"
        params = {"api_key": settings.tmdb_api_key}
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
        rows = []
        for item in data.get("results", []):
            content = self.normalize_text(item.get("content", ""))
            if not content:
                continue
            rows.append(
                NormalizedReview(
                    platform=self.platform,
                    text=content,
                    author=item.get("author"),
                    language=item.get("iso_639_1") or "en",
                    source_url=item.get("url"),
                    posted_at=self.parse_dt(item.get("created_at")),
                )
            )
        return rows


class OMDBSource(BaseReviewSource):
    platform = "omdb"

    async def fetch_reviews(self, query: str) -> list[NormalizedReview]:
        if not settings.omdb_api_key:
            return []
        # OMDb returns aggregate ratings, not full user review text.
        # Convert rating providers into normalized pseudo-reviews for cross-platform weighting.
        url = "https://www.omdbapi.com/"
        params = {"apikey": settings.omdb_api_key, "t": query}
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
        if data.get("Response") != "True":
            return []
        rows = []
        for rating in data.get("Ratings", []):
            rows.append(
                NormalizedReview(
                    platform=self.platform,
                    text=f'{rating.get("Source")} rating for {data.get("Title")}: {rating.get("Value")}',
                    author=rating.get("Source"),
                    language="en",
                    source_url=data.get("Website") if data.get("Website") not in {"N/A", None} else None,
                )
            )
        return rows


class RedditSource(BaseReviewSource):
    platform = "reddit"

    async def fetch_reviews(self, query: str) -> list[NormalizedReview]:
        if not settings.reddit_client_id or not settings.reddit_client_secret:
            return []
        reddit = asyncpraw.Reddit(
            client_id=settings.reddit_client_id,
            client_secret=settings.reddit_client_secret,
            user_agent=settings.reddit_user_agent,
        )
        subreddits = ["movies", "bollywood", "BollyBlindsNGossip"]
        reviews: list[NormalizedReview] = []
        for sub in subreddits:
            subreddit = await reddit.subreddit(sub)
            async for submission in subreddit.search(query, limit=15, sort="relevance"):
                body = self.normalize_text(submission.title + " " + (submission.selftext or ""))
                if len(body) < 20:
                    continue
                reviews.append(
                    NormalizedReview(
                        platform=self.platform,
                        text=body,
                        author=str(submission.author) if submission.author else None,
                        source_url=f"https://reddit.com{submission.permalink}",
                        posted_at=datetime_from_epoch(submission.created_utc),
                    )
                )
        await reddit.close()
        return reviews


def datetime_from_epoch(value: float | int | None):
    from datetime import datetime, timezone

    if value is None:
        return None
    return datetime.fromtimestamp(float(value), tz=timezone.utc)
