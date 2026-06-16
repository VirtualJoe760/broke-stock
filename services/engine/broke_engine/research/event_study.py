"""L2 event study: does a signal predict forward returns, after costs?

Pipeline: for each (date, ticker, headline) → score via the LLM → Signal; join to the
realized forward return from a PointInTimeStore; for events that clear the surprise gate,
treat positive sentiment as a long and negative as a short; net out transaction costs;
report the long-short spread, a pooled per-signal mean return, and a crude t-stat.

HONEST LIMITS (see docs/05-research/validation-methodology.md):
- Synthetic prices => numbers are meaningless (pipeline test only).
- Real verdict needs REAL point-in-time news + prices, post-training-cutoff dates (leakage),
  a meaningful sample size, and out-of-sample confirmation. Small N => preliminary, not proof.
"""

from __future__ import annotations

import math
import statistics
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
    n: int  # events with a forward return
    horizon_days: int
    n_long: int
    n_short: int
    long_avg_return_pct: float
    short_avg_return_pct: float
    long_short_spread_pct: float  # gross (long_avg - short_avg)
    cost_bps_per_leg: float
    net_spread_pct: float  # gross spread minus 2 legs of cost
    mean_signal_return_pct: float  # pooled per-signal net return (long: fwd-cost; short: -fwd-cost)
    t_stat: float  # crude significance of the pooled signal returns
    outcomes: list[EventOutcome] = field(default_factory=list)
    note: str = (
        "PRELIMINARY unless run on real point-in-time news + prices, post-cutoff dates, "
        "and a meaningful sample. Synthetic data => meaningless."
    )


def forward_return_pct(
    store: PointInTimeStore, ticker: str, date: datetime, horizon_days: int
) -> float | None:
    """Realized return from the first bar on/after `date` to `horizon_days` trading bars later."""
    end = date + timedelta(days=horizon_days * 2 + 10)
    bars = store.get_bars(ticker, date - timedelta(days=5), end, as_of=end)
    future = [b for b in bars if b.ts >= date]
    if len(future) <= horizon_days:
        return None
    return (future[horizon_days].close / future[0].close - 1) * 100


def run_event_study(
    events: list[NewsEvent],
    provider: LLMProvider,
    store: PointInTimeStore,
    horizon_days: int = 5,
    surprise_threshold: float = 0.5,
    cost_bps_per_leg: float = 10.0,
) -> EventStudyResult:
    cost_pct = cost_bps_per_leg / 100.0  # 10 bps -> 0.10 (%)
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
    gross = la - sa
    net = gross - 2 * cost_pct

    # Pooled per-signal net returns: long = fwd - cost; short = -fwd - cost
    pooled = [r - cost_pct for r in longs] + [-r - cost_pct for r in shorts]
    mean_ret = sum(pooled) / len(pooled) if pooled else 0.0
    if len(pooled) > 1:
        sd = statistics.pstdev(pooled)
        t_stat = mean_ret / (sd / math.sqrt(len(pooled))) if sd > 0 else 0.0
    else:
        t_stat = 0.0

    return EventStudyResult(
        n=len(outcomes),
        horizon_days=horizon_days,
        n_long=len(longs),
        n_short=len(shorts),
        long_avg_return_pct=round(la, 3),
        short_avg_return_pct=round(sa, 3),
        long_short_spread_pct=round(gross, 3),
        cost_bps_per_leg=cost_bps_per_leg,
        net_spread_pct=round(net, 3),
        mean_signal_return_pct=round(mean_ret, 3),
        t_stat=round(t_stat, 2),
    )


@dataclass(frozen=True)
class DirectionalEvent:
    date: datetime
    ticker: str
    direction: int  # +1 = long, -1 = short
    label: str = ""


@dataclass
class DirectionalResult:
    n: int
    horizon_days: int
    n_long: int
    n_short: int
    long_avg_return_pct: float
    short_avg_return_pct: float
    gross_spread_pct: float
    cost_bps_per_leg: float
    net_spread_pct: float
    mean_signal_return_pct: float
    t_stat: float


def run_directional_study(
    events: list[DirectionalEvent],
    store: PointInTimeStore,
    horizon_days: int = 5,
    cost_bps_per_leg: float = 10.0,
) -> DirectionalResult:
    """Event study for events that already carry a direction (e.g. analyst up/downgrades).

    No LLM. Long the +1s, short the -1s; net out costs; report spread + pooled t-stat.
    """
    cost = cost_bps_per_leg / 100.0
    longs: list[float] = []
    shorts: list[float] = []
    pooled: list[float] = []
    for e in events:
        r = forward_return_pct(store, e.ticker, e.date, horizon_days)
        if r is None:
            continue
        if e.direction > 0:
            longs.append(r)
            pooled.append(r - cost)
        elif e.direction < 0:
            shorts.append(r)
            pooled.append(-r - cost)

    la = sum(longs) / len(longs) if longs else 0.0
    sa = sum(shorts) / len(shorts) if shorts else 0.0
    gross = la - sa
    mean_ret = sum(pooled) / len(pooled) if pooled else 0.0
    if len(pooled) > 1:
        sd = statistics.pstdev(pooled)
        t_stat = mean_ret / (sd / math.sqrt(len(pooled))) if sd > 0 else 0.0
    else:
        t_stat = 0.0

    return DirectionalResult(
        n=len(longs) + len(shorts),
        horizon_days=horizon_days,
        n_long=len(longs),
        n_short=len(shorts),
        long_avg_return_pct=round(la, 3),
        short_avg_return_pct=round(sa, 3),
        gross_spread_pct=round(gross, 3),
        cost_bps_per_leg=cost_bps_per_leg,
        net_spread_pct=round(gross - 2 * cost, 3),
        mean_signal_return_pct=round(mean_ret, 3),
        t_stat=round(t_stat, 2),
    )

