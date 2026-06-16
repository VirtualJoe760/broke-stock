"""REAL L2 v2: catalyst-filtered, date-diverse, cost-adjusted edge test.

Real Polygon news + prices, Claude scoring, post-cutoff window (Feb–May 2026), ~10 names.
Filters headlines to company-specific catalysts, caps to diverse dates, models costs, prints
a long-short spread + t-stat. Still PRELIMINARY (free-tier data, modest N) — not proof.
Requires POLYGON_API_KEY + ANTHROPIC_API_KEY. Run from services/engine.
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

TICKERS = ["AAPL", "NVDA", "MSFT", "AMZN", "AMD", "META", "GOOGL", "TSLA", "AVGO", "MU"]
NEWS_START = datetime(2026, 2, 1, tzinfo=timezone.utc)
NEWS_END = datetime(2026, 5, 15, tzinfo=timezone.utc)
PRICE_START = datetime(2026, 1, 25, tzinfo=timezone.utc)
PRICE_END = datetime(2026, 5, 31, tzinfo=timezone.utc)
PER_TICKER = 6
RATE_SLEEP = 13

CATALYSTS = (
    "earnings", "beats", "beat ", "misses", "miss ", "guidance", "raises", "raised",
    "cuts", "lowers", "downgrade", "upgrade", "initiated", "price target", "acqui",
    "merger", "buyout", "lawsuit", "sues", "settle", "probe", "investigation", "recall",
    "approval", "approved", "partnership", "contract", "layoff", "restructur", "warning",
    "results", "revenue", "forecast", "outlook", "dividend", "buyback", "soars", "plunges",
    "surges", "tumbles", "jumps", "drops", "warns",
)


def is_catalyst(title: str) -> bool:
    t = title.lower()
    return any(k in t for k in CATALYSTS)


class PreloadedStore(PointInTimeStore):
    def __init__(self) -> None:
        self.data: dict[str, list[Bar]] = {}

    def add(self, ticker: str, bars: list[Bar]) -> None:
        self.data[ticker] = sorted(bars, key=lambda b: b.ts)

    def get_bars(self, symbol: str, start: datetime, end: datetime, as_of: datetime) -> list[Bar]:
        return [b for b in self.data.get(symbol, []) if start <= b.ts <= end and b.ingest_ts <= as_of]


def diverse(news: list[tuple[datetime, str]], cap: int) -> list[tuple[datetime, str]]:
    seen_days: set = set()
    out: list[tuple[datetime, str]] = []
    for dt, title in news:
        if not is_catalyst(title):
            continue
        day = dt.date()
        if day in seen_days:
            continue
        seen_days.add(day)
        out.append((dt, title))
        if len(out) >= cap:
            break
    return out


def main() -> None:
    poly = PolygonPointInTimeStore()
    store = PreloadedStore()
    events: list[NewsEvent] = []

    for t in TICKERS:
        bars = poly.get_bars(t, PRICE_START, PRICE_END, as_of=PRICE_END)
        store.add(t, bars)
        time.sleep(RATE_SLEEP)
        raw = fetch_news(t, NEWS_START, NEWS_END, limit=50)
        picked = diverse(raw, PER_TICKER)
        for dt, title in picked:
            events.append(NewsEvent(dt, t, title))
        print(f"{t}: {len(bars)} bars, {len(raw)} headlines -> {len(picked)} catalysts", flush=True)
        time.sleep(RATE_SLEEP)

    print(f"total catalyst events: {len(events)}; scoring via Claude...", flush=True)
    res = run_event_study(events, get_provider(), store, horizon_days=5, surprise_threshold=0.4, cost_bps_per_leg=10.0)

    print("=" * 68, flush=True)
    for o in res.outcomes:
        flag = "L" if (o.surprise >= 0.4 and o.sentiment > 0) else ("S" if (o.surprise >= 0.4 and o.sentiment < 0) else ".")
        print(f"[{flag}] {o.ticker:5} surprise={o.surprise:.2f} sentiment={o.sentiment:+.2f} fwd5d={o.fwd_return_pct:+.2f}%", flush=True)
    print("=" * 68, flush=True)
    print(f"events={res.n}  signals: {res.n_long} long / {res.n_short} short", flush=True)
    print(f"long_avg={res.long_avg_return_pct}%  short_avg={res.short_avg_return_pct}%", flush=True)
    print(f"gross_spread={res.long_short_spread_pct}%  net_spread(after {res.cost_bps_per_leg}bps/leg)={res.net_spread_pct}%", flush=True)
    print(f"pooled mean signal return={res.mean_signal_return_pct}%  t-stat={res.t_stat}", flush=True)
    print("VERDICT GUIDE: |t|<2 => not significant. Small N + free-tier news => PRELIMINARY.", flush=True)


if __name__ == "__main__":
    main()
