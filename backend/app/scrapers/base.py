from __future__ import annotations

import asyncio
import random
import re
from dataclasses import dataclass
from datetime import datetime
from urllib import robotparser
from urllib.parse import urlparse

import httpx


USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)",
]


@dataclass
class NormalizedReview:
    platform: str
    text: str
    rating: float | None = None
    author: str | None = None
    language: str = "en"
    posted_at: datetime | None = None
    source_url: str | None = None


class BaseReviewSource:
    platform: str = "unknown"
    crawl_delay_seconds: float = 1.0
    retries: int = 2

    async def can_fetch(self, url: str) -> bool:
        parts = urlparse(url)
        robots_url = f"{parts.scheme}://{parts.netloc}/robots.txt"
        rp = robotparser.RobotFileParser()
        rp.set_url(robots_url)
        try:
            rp.read()
            return rp.can_fetch(USER_AGENTS[0], url)
        except Exception:
            return True

    async def fetch_json(self, url: str) -> dict:
        for attempt in range(self.retries + 1):
            try:
                headers = {"User-Agent": random.choice(USER_AGENTS)}
                async with httpx.AsyncClient(timeout=20.0, headers=headers) as client:
                    resp = await client.get(url)
                    resp.raise_for_status()
                    await asyncio.sleep(self.crawl_delay_seconds)
                    return resp.json()
            except Exception:
                if attempt == self.retries:
                    raise
        return {}

    @staticmethod
    def normalize_text(text: str) -> str:
        cleaned = re.sub(r"\s+", " ", text).strip()
        return cleaned

    @staticmethod
    def parse_dt(value: str | None) -> datetime | None:
        if not value:
            return None
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except Exception:
            return None

    async def fetch_reviews(self, query: str) -> list[NormalizedReview]:
        raise NotImplementedError
