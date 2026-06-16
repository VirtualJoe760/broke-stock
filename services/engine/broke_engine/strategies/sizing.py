"""Signal aggregation (time-decay) + volatility-scaled position sizing.

Deterministic math — the LLM scores, this sizes. Parameters here are validated by
walk-forward, not hand-picked. See docs/01-architecture/strategy-and-sizing.md.
"""

from __future__ import annotations

import statistics
from dataclasses import dataclass

from ..signals.models import Signal


def decayed_score(signals: list[tuple[Signal, float]], half_life_days: float = 5.0) -> float:
    """Aggregate per-ticker signals into a directional score in [-1, 1].

    Each item is (signal, age_in_days). Recent signals weigh more (exponential
    half-life) and higher-confidence signals weigh more. The per-signal contribution
    is sentiment * surprise (surprise is the alpha-bearing, not-yet-priced-in part).
    """
    if not signals:
        return 0.0
    num = 0.0
    den = 0.0
    for s, age in signals:
        weight = (0.5 ** (max(0.0, age) / half_life_days)) * s.confidence
        num += weight * (s.sentiment * s.surprise)
        den += weight
    return num / den if den > 0 else 0.0


def daily_volatility_pct(closes: list[float]) -> float:
    """Population stdev of daily returns, in percent."""
    if len(closes) < 2:
        return 0.0
    rets = [closes[i] / closes[i - 1] - 1 for i in range(1, len(closes))]
    return statistics.pstdev(rets) * 100


@dataclass
class SizingParams:
    max_position_pct: float = 5.0  # hard cap per position (also re-checked at the risk gate)
    target_vol_pct: float = 2.0  # per-position daily-vol target
    min_score: float = 0.1  # below this conviction, take no position


def target_weight(score: float, daily_vol_pct: float, params: SizingParams | None = None) -> float:
    """Target position weight as % of equity (signed). Vol-scaled and capped.

    Lower-volatility names get larger size for the same conviction; the result is
    clamped to ±max_position_pct.
    """
    p = params or SizingParams()
    if abs(score) < p.min_score or daily_vol_pct <= 0:
        return 0.0
    raw = score * p.max_position_pct * (p.target_vol_pct / daily_vol_pct)
    return max(-p.max_position_pct, min(p.max_position_pct, raw))
