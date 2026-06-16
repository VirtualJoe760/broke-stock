"""L2 (factor test): do analyst UP/DOWNGRADES predict forward returns?

Real FMP analyst rating changes + real Polygon prices. NO LLM (pure factor test).
Post-cutoff window (Feb–May 2026). Long upgrades, short downgrades, net costs, t-stat.
Requires FMP_API_KEY + POLYGON_API_KEY. Run from services/engine.
"""

from __future__ import annotations

import time
from datetime import datetime, timezone

from broke_engine.data.fmp_grades import fetch_grade_changes
from broke_engine.data.models import Bar
from broke_engine.data.polygon_store import PolygonPointInTimeStore
from broke_engine.data.store import PointInTimeStore
from broke_engine.research import DirectionalEvent, run_directional_study

TICKERS = ["AAPL", "NVDA", "MSFT", "AMZN", "AMD", "META", "GOOGL", "TSLA", "AVGO", "MU", "NFLX", "CRM"]
START = datetime(2026, 2, 1, tzinfo=timezone.utc)
END = datetime(2026, 5, 10, tzinfo=timezone.utc)
PRICE_START = datetime(2026, 1, 25, tzinfo=timezone.utc)
PRICE_END = datetime(2026, 5, 31, tzinfo=timezone.utc)
RATE_SLEEP = 13


class PreloadedStore(PointInTimeStore):
    def __init__(self) -> None:
        self.data: dict[str, list[Bar]] = {}

    def add(self, ticker: str, bars: list[Bar]) -> None:
        self.data[ticker] = sorted(bars, key=lambda b: b.ts)

    def get_bars(self, symbol: str, start: datetime, end: datetime, as_of: datetime) -> list[Bar]:
        return [b for b in self.data.get(symbol, []) if start <= b.ts <= end and b.ingest_ts <= as_of]


def main() -> None:
    poly = PolygonPointInTimeStore()
    store = PreloadedStore()
    events: list[DirectionalEvent] = []

    for t in TICKERS:
        try:
            bars = poly.get_bars(t, PRICE_START, PRICE_END, as_of=PRICE_END)
            store.add(t, bars)
        except Exception as e:
            print(f"{t}: price fetch failed ({type(e).__name__}), skipping", flush=True)
            time.sleep(RATE_SLEEP)
            continue
        try:
            changes = fetch_grade_changes(t, START, END)
        except Exception as e:
            print(f"{t}: grades unavailable ({e})", flush=True)
            changes = []
        ups = sum(1 for _, d, _ in changes if d > 0)
        downs = sum(1 for _, d, _ in changes if d < 0)
        for dt, direction, label in changes:
            events.append(DirectionalEvent(dt, t, direction, label))
        print(f"{t}: {len(bars)} bars | {ups} upgrades / {downs} downgrades", flush=True)
        time.sleep(RATE_SLEEP)

    print(f"total grade-change events: {len(events)}", flush=True)
    res = run_directional_study(events, store, horizon_days=5, cost_bps_per_leg=10.0)
    print("=" * 64, flush=True)
    print(f"events={res.n}  ({res.n_long} upgrades long / {res.n_short} downgrades short)", flush=True)
    print(f"upgrade avg fwd5d={res.long_avg_return_pct}%   downgrade avg fwd5d={res.short_avg_return_pct}%", flush=True)
    print(f"gross_spread={res.gross_spread_pct}%   net_spread(after {res.cost_bps_per_leg}bps/leg)={res.net_spread_pct}%", flush=True)
    print(f"pooled mean signal return={res.mean_signal_return_pct}%   t-stat={res.t_stat}", flush=True)
    print("VERDICT GUIDE: |t|>=2 => significant. Free-tier prices + ~3mo window => still preliminary.", flush=True)


if __name__ == "__main__":
    main()
