"""L2 event study: does a signal predict forward returns?

Pipeline: for each (date, ticker, headline) → score via the LLM → Signal; join to the
realized forward return from a PointInTimeStore; bucket by surprise + sentiment; report
mean forward return for high-surprise longs vs shorts and the long-short spread.

HONEST LIMITS (see docs/05-research/validation-methodology.md):
- With MockPointInTimeStore (synthetic random prices) this only proves the PIPELINE runs;
  the numbers mean NOTHING about real edge.
- A real verdict needs REAL point-in-time news + prices (Alpaca/Polygon) AND dates AFTER the
  model's training cutoff, or the LLM may "remember" outcomes (data leakage).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta

from ..data.store import PointInTimeStore
from ..llm.provider import LLMProvider
from ..signals.scorer import score_news


@dataclass(frozen=True)
class NewsEvent:
    date: datetime
    ticker: str
    headline: str
    context: str = ""


@dataclass
class EventOutcome:
    ticker: str
    surprise: float
    sentiment: float
    fwd_return_pct: float


@dataclass
class EventStudyResult:
    n: int
    horizon_days: int
    long_avg_return_pct: float
    short_avg_return_pct: float
    long_short_spread_pct: float
    outcomes: list[EventOutcome] = field(default_factory=list)
    note: str = (
        "PIPELINE TEST ONLY unless run on real point-in-time news + prices and "
        "post-training-cutoff dates. Synthetic data => numbers are meaningless."
    )


def forward_return_pct(
    store: PointInTimeStore, ticker: str, date: datetime, horizon_days: int
) -> float | None:
    """Realized return from the first bar on/after `date` to `horizon_days` trading bars later.

    Uses future data deliberately — an event study *measures* whether the signal predicted
    the move. Returns None if there aren't enough bars.
    """
    end = date + timedelta(days=horizon_days * 2 + 7)  # buffer for weekends
    bars = store.get_bars(ticker, date - timedelta(days=5), end, as_of=end)
    future = [b for b in bars if b.ts >= date]
    if len(future) <= horizon_days:
        return None
    entry = future[0].close
    exit_ = future[horizon_days].close
    return (exit_ / entry - 1) * 100


def run_event_study(
    events: list[NewsEvent],
    provider: LLMProvider,
    store: PointInTimeStore,
    horizon_days: int = 5,
    surprise_threshold: float = 0.5,
) -> EventStudyResult:
    outcomes: list[EventOutcome] = []
    for e in events:
        signal = score_news(provider, e.ticker, e.headline, e.context)
        r = forward_return_pct(store, e.ticker, e.date, horizon_days)
        if r is None:
            continue
        outcomes.append(EventOutcome(e.ticker, signal.surprise, signal.sentiment, r))

    longs = [o.fwd_return_pct for o in outcomes if o.surprise >= surprise_threshold and o.sentiment > 0]
    shorts = [o.fwd_return_pct for o in outcomes if o.surprise >= surprise_threshold and o.sentiment < 0]
    la = sum(longs) / len(longs) if longs else 0.0
    sa = sum(shorts) / len(shorts) if shorts else 0.0

    return EventStudyResult(
        n=len(outcomes),
        horizon_days=horizon_days,
        long_avg_return_pct=round(la, 3),
        short_avg_return_pct=round(sa, 3),
        long_short_spread_pct=round(la - sa, 3),
        outcomes=outcomes,
    )
