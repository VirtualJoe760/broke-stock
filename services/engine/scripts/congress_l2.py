"""Validate: do congressional trades (entered on the DISCLOSURE date) predict forward returns?

Real congress feed (FMP) + real prices (Polygon). NO LLM. Buys = long, sells = short.
HONEST: the free 'latest' feed is recent + shallow, so many events won't have enough
realized forward price data yet -> likely too small to conclude. Requires FMP + POLYGON keys.
Run from services/engine.
"""

from __future__ import annotations

import time
from datetime import datetime, timezone

from broke_engine.data.congress import fetch_congress_trades
from broke_engine.data.polygon_store import PolygonPointInTimeStore
from broke_engine.data.store import PointInTimeStore
from broke_engine.research import DirectionalEvent, run_directional_study

HORIZON = 3
PRICE_START = datetime(2026, 4, 15, tzinfo=timezone.utc)
PRICE_END = datetime(2026, 6, 16, tzinfo=timezone.utc)
RATE_SLEEP = 13


class PreloadedStore(PointInTimeStore):
    def __init__(self) -> None:
        self.data = {}

    def add(self, t, bars) -> None:
        self.data[t] = sorted(bars, key=lambda b: b.ts)

    def get_bars(self, sym, start, end, as_of):
        return [b for b in self.data.get(sym, []) if start <= b.ts <= end and b.ingest_ts <= as_of]


def main() -> None:
    trades = fetch_congress_trades(limit=25, pages=4)
    events = []
    for t in trades:
        if t.transaction_type not in ("buy", "sell") or not t.disclosure_date:
            continue
        try:
            dt = datetime.fromisoformat(t.disclosure_date[:10]).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
        events.append(DirectionalEvent(dt, t.symbol, 1 if t.transaction_type == "buy" else -1, t.member))

    tickers = sorted({e.ticker for e in events})
    print(f"{len(events)} congressional events across {len(tickers)} tickers; fetching prices...", flush=True)
    poly = PolygonPointInTimeStore()
    store = PreloadedStore()
    for tk in tickers:
        try:
            store.add(tk, poly.get_bars(tk, PRICE_START, PRICE_END, as_of=PRICE_END))
        except Exception as e:
            print(f"  {tk}: price fetch failed ({type(e).__name__})", flush=True)
        time.sleep(RATE_SLEEP)

    res = run_directional_study(events, store, horizon_days=HORIZON, cost_bps_per_leg=10.0)
    print("=" * 60, flush=True)
    print(f"events with realized return = {res.n}  ({res.n_long} buys / {res.n_short} sells)  horizon={HORIZON}d", flush=True)
    print(f"buy avg={res.long_avg_return_pct}%  sell avg={res.short_avg_return_pct}%", flush=True)
    print(f"net_spread(after costs)={res.net_spread_pct}%  t-stat={res.t_stat}", flush=True)
    print("HONEST: free feed is recent+shallow; most disclosures lack realized forward data. Likely inconclusive => needs paid history to validate properly.", flush=True)


if __name__ == "__main__":
    main()
