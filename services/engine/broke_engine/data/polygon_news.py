"""Fetch real news headlines from Polygon/Massive (/v2/reference/news).

Returns (published_datetime, title) tuples. Requires POLYGON_API_KEY.
"""

from __future__ import annotations

from datetime import datetime

import httpx

from ..config import settings


def fetch_news(
    ticker: str,
    start: datetime,
    end: datetime,
    limit: int = 10,
    api_key: str | None = None,
    base_url: str | None = None,
    timeout: float = 20.0,
) -> list[tuple[datetime, str]]:
    api_key = api_key or settings.polygon_api_key
    base = (base_url or settings.polygon_base_url).rstrip("/")
    resp = httpx.get(
        f"{base}/v2/reference/news",
        params={
            "ticker": ticker,
            "published_utc.gte": start.date().isoformat(),
            "published_utc.lte": end.date().isoformat(),
            "order": "asc",
            "sort": "published_utc",
            "limit": limit,
            "apiKey": api_key,
        },
        timeout=timeout,
    )
    resp.raise_for_status()
    out: list[tuple[datetime, str]] = []
    for a in resp.json().get("results", []) or []:
        pub, title = a.get("published_utc"), a.get("title")
        if not pub or not title:
            continue
        out.append((datetime.fromisoformat(pub.replace("Z", "+00:00")), title))
    return out
