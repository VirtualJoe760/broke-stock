"""Run the L2 event-study PIPELINE end-to-end: real Claude scoring + MOCK prices.

NOTE: prices are synthetic, so the forward returns are MEANINGLESS — this proves the
pipeline runs, not that there is edge. A real study needs Alpaca/Polygon point-in-time
data and post-training-cutoff dates. Requires ANTHROPIC_API_KEY.
Run from services/engine:  python scripts/event_study_demo.py
"""

from datetime import datetime, timezone

from broke_engine.data.store import MockPointInTimeStore
from broke_engine.llm import get_provider
from broke_engine.research import NewsEvent, run_event_study

EVENTS = [
    NewsEvent(datetime(2024, 2, 1, tzinfo=timezone.utc), "NVDA", "Company raises full-year revenue guidance well above consensus"),
    NewsEvent(datetime(2024, 2, 1, tzinfo=timezone.utc), "AAPL", "Analyst downgrades to sell on slowing iPhone demand"),
    NewsEvent(datetime(2024, 2, 1, tzinfo=timezone.utc), "MU", "Memory chip prices surge on AI server demand"),
]


def main() -> None:
    result = run_event_study(EVENTS, get_provider(), MockPointInTimeStore(), horizon_days=5)
    print(f"n={result.n}  horizon={result.horizon_days}d")
    for o in result.outcomes:
        print(f"  {o.ticker}: surprise={o.surprise}  sentiment={o.sentiment}  fwd_return={o.fwd_return_pct:.2f}%")
    print(f"long_avg={result.long_avg_return_pct}%  short_avg={result.short_avg_return_pct}%  spread={result.long_short_spread_pct}%")
    print("NOTE:", result.note)


if __name__ == "__main__":
    main()
