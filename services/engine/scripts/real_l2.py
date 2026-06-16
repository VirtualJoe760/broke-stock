"""REAL(er) L2 event study: real Polygon news + real Polygon prices + Claude scoring.

Uses a POST-training-cutoff window (May 2026, after the model's Jan-2026 cutoff) to limit
data leakage. Small sample + noisy general-market headlines + free-tier data => PRELIMINARY,
NOT statistically conclusive. Requires POLYGON_API_KEY + ANTHROPIC_API_KEY.

Run from services/engine:  python scripts/real_l2.py
"""

from __future__ import annotations

import time
from datetime import datetime, timezone

from broke_engine.data.models import Bar
from broke_engine.data.polygon_news import fetch_news
from broke_engine.data.polygon_store import PolygonPointInTimeStore
from broke_engine.data.store import PointInTimeStore
from broke_engine.llm import get_provider
from broke_engine.research import NewsEvent, run_event_study

TICKERS = ["AAPL", "NVDA", "MSFT", "AMZN", "AMD"]
NEWS_START = datetime(2026, 5, 1, tzinfo=timezone.utc)
NEWS_END = datetime(2026, 5, 9, tzinfo=timezone.utc)
PRICE_START = datetime(2026, 4, 25, tzinfo=timezone.utc)
PRICE_END = datetime(2026, 5, 30, tzinfo=timezone.utc)
PER_TICKER = 3
RATE_SLEEP = 13  # free tier ~5 req/min


class PreloadedStore(PointInTimeStore):
    """In-memory store so the event study makes zero extra API calls (rate-limit safe)."""

    def __init__(self) -> None:
        self.data: dict[str, list[Bar]] = {}

    def add(self, ticker: str, bars: list[Bar]) -> None:
        self.data[ticker] = sorted(bars, key=lambda b: b.ts)

    def get_bars(self, symbol: str, start: datetime, end: datetime, as_of: datetime) -> list[Bar]:
        return [b for b in self.data.get(symbol, []) if start <= b.ts <= end and b.ingest_ts <= as_of]


def main() -> None:
    poly = PolygonPointInTimeStore()
    store = PreloadedStore()
    events: list[NewsEvent] = []

    for t in TICKERS:
        bars = poly.get_bars(t, PRICE_START, PRICE_END, as_of=PRICE_END)
        store.add(t, bars)
        time.sleep(RATE_SLEEP)
        news = fetch_news(t, NEWS_START, NEWS_END, limit=PER_TICKER)
        for dt, title in news[:PER_TICKER]:
            events.append(NewsEvent(dt, t, title))
        print(f"{t}: {len(bars)} bars, {min(len(news), PER_TICKER)} headlines")
        time.sleep(RATE_SLEEP)

    print(f"total events: {len(events)}; scoring via Claude...")
    res = run_event_study(events, get_provider(), store, horizon_days=5, surprise_threshold=0.5)
    print("=" * 64)
    for o in res.outcomes:
        print(f"{o.ticker:5} surprise={o.surprise:.2f} sentiment={o.sentiment:+.2f} fwd5d={o.fwd_return_pct:+.2f}%")
    print("=" * 64)
    print(f"n={res.n} | long_avg={res.long_avg_return_pct}%  short_avg={res.short_avg_return_pct}%  SPREAD={res.long_short_spread_pct}%")
    print("PRELIMINARY: tiny sample, noisy general-market headlines, free-tier data — not conclusive.")


if __name__ == "__main__":
    main()
