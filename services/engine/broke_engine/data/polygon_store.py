"""Polygon (rebranded 'Massive') daily-bar price source implementing PointInTimeStore.

Free tier: end-of-day aggregates, ~5 req/min, limited history — fine for a small L2.
Requires POLYGON_API_KEY. Host defaults to api.polygon.io; if the Massive rebrand moves
the API, set POLYGON_BASE_URL (e.g. https://api.massive.com).

UNVERIFIED until run with a real key + network — endpoint/host may need adjustment.
Point-in-time: only returns bars with ts <= as_of (forward-return research passes a
future as_of deliberately to measure realized returns).
"""

from __future__ import annotations

import time
from datetime import datetime, timezone

import httpx

from ..config import settings
from .models import Bar
from .store import PointInTimeStore


class PolygonPointInTimeStore(PointInTimeStore):
    def __init__(
        self, api_key: str | None = None, base_url: str | None = None, timeout: float = 30.0, retries: int = 3
    ) -> None:
        self.api_key = api_key or settings.polygon_api_key
        self.base_url = (base_url or settings.polygon_base_url).rstrip("/")
        self.timeout = timeout
        self.retries = retries
        if not self.api_key:
            raise ValueError("POLYGON_API_KEY is required for PolygonPointInTimeStore")

    def get_bars(self, symbol: str, start: datetime, end: datetime, as_of: datetime) -> list[Bar]:
        url = f"{self.base_url}/v2/aggs/ticker/{symbol}/range/1/day/{start.date()}/{end.date()}"
        params = {"adjusted": "true", "sort": "asc", "limit": 50000, "apiKey": self.api_key}
        resp = None
        for attempt in range(self.retries):
            try:
                resp = httpx.get(url, params=params, timeout=self.timeout)
                break
            except httpx.TimeoutException:
                if attempt == self.retries - 1:
                    raise
                time.sleep(2 * (attempt + 1))
        assert resp is not None
        resp.raise_for_status()
        results = resp.json().get("results", []) or []
        bars: list[Bar] = []
        for it in results:
            ts = datetime.fromtimestamp(it["t"] / 1000, tz=timezone.utc)
            if ts <= as_of:
                bars.append(
                    Bar(
                        symbol=symbol,
                        ts=ts,
                        open=it["o"],
                        high=it["h"],
                        low=it["l"],
                        close=it["c"],
                        volume=it.get("v", 0),
                        ingest_ts=ts,
                    )
                )
        return bars
