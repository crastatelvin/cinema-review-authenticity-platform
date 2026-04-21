from __future__ import annotations

from typing import Iterable

import httpx
from selectolax.parser import HTMLParser

from app.core.config import settings
from app.scrapers.base import BaseReviewSource, NormalizedReview


class ScrapedSource(BaseReviewSource):
    allowed_domains: tuple[str, ...] = tuple()
    selectors: tuple[str, ...] = tuple()

    async def fetch_html(self, url: str) -> str:
        if not await self.can_fetch(url):
            return ""
        headers = {"User-Agent": "Mozilla/5.0"}
        async with httpx.AsyncClient(timeout=25.0, headers=headers, follow_redirects=True) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            return resp.text

    def parse_candidates(self, html: str) -> list[str]:
        tree = HTMLParser(html)
        values: list[str] = []
        for sel in self.selectors:
            for node in tree.css(sel):
                text = self.normalize_text(node.text())
                if len(text) >= 40:
                    values.append(text)
        if not values:
            # Generic fallback for semi-structured article/review pages.
            for node in tree.css("p"):
                text = self.normalize_text(node.text())
                if len(text) >= 80:
                    values.append(text)
        deduped = list(dict.fromkeys(values))
        return deduped[:100]

    async def fetch_reviews(self, query: str) -> list[NormalizedReview]:
        if not settings.enable_scraped_sources:
            return []
        if not query.startswith("http"):
            return []
        if self.allowed_domains and not any(domain in query for domain in self.allowed_domains):
            return []
        html = await self.fetch_html(query)
        if not html:
            return []
        return [
            NormalizedReview(
                platform=self.platform,
                text=text,
                source_url=query,
            )
            for text in self.parse_candidates(html)
        ]


class GenericReviewPageSource(ScrapedSource):
    platform = "generic_web"
    allowed_domains = tuple()
    selectors = ("article p", ".review p", ".comment p", "main p", "p")

    async def fetch_reviews(self, query: str) -> list[NormalizedReview]:
        if not settings.enable_scraped_sources or not query.startswith("http"):
            return []
        # User explicitly supplied this URL, so we allow a best-effort parse even
        # when robots rules are restrictive for generic crawling.
        headers = {"User-Agent": "Mozilla/5.0"}
        async with httpx.AsyncClient(timeout=25.0, headers=headers, follow_redirects=True) as client:
            resp = await client.get(query)
            resp.raise_for_status()
            html = resp.text
        if not html:
            return []
        rows = [
            NormalizedReview(platform=self.platform, text=text, source_url=query)
            for text in self.parse_candidates(html)
        ]
        return rows[:120]


class IMDBSource(ScrapedSource):
    platform = "imdb"
    allowed_domains = ("imdb.com",)
    selectors = ('[data-testid="review-container"] .ipc-html-content-inner-div', ".text.show-more__control")


class RottenTomatoesSource(ScrapedSource):
    platform = "rotten_tomatoes"
    allowed_domains = ("rottentomatoes.com",)
    selectors = ('[data-qa="review-quote"]', ".review-text", ".audience-reviews__review")


class MetacriticSource(ScrapedSource):
    platform = "metacritic"
    allowed_domains = ("metacritic.com",)
    selectors = (".c-siteReview_quote", ".c-pageProductReviews_row .c-siteReview", ".review_body")


class LetterboxdSource(ScrapedSource):
    platform = "letterboxd"
    allowed_domains = ("letterboxd.com",)
    selectors = (".review .body-text", ".film-detail-content .body-text", ".review .js-review-body")


class BookMyShowSource(ScrapedSource):
    platform = "bookmyshow"
    allowed_domains = ("bookmyshow.com",)
    selectors = (".review-text", '[data-testid="review-text"]', ".styles__ReviewText")


class KoimoiSource(ScrapedSource):
    platform = "koimoi"
    allowed_domains = ("koimoi.com",)
    selectors = (".entry-content p", ".user-review p", ".review p")


class BollywoodHungamaSource(ScrapedSource):
    platform = "bollywood_hungama"
    allowed_domains = ("bollywoodhungama.com",)
    selectors = (".userreview", ".bh-review-content p", ".review-content p")


class TimesOfIndiaSource(ScrapedSource):
    platform = "times_of_india"
    allowed_domains = ("timesofindia.indiatimes.com",)
    selectors = (".review_content", ".Normal", ".js_tbl_row p")
