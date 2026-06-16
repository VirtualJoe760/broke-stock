"""Signal aggregation + vol-scaled sizing."""

from broke_engine.signals.models import EventType, Magnitude, Signal, TimeHorizon
from broke_engine.strategies import (
    SizingParams,
    daily_volatility_pct,
    decayed_score,
    target_weight,
)


def _sig(sentiment: float, surprise: float, confidence: float) -> Signal:
    return Signal(
        ticker="X",
        event_type=EventType.OTHER,
        sentiment=sentiment,
        surprise=surprise,
        magnitude=Magnitude.MODERATE,
        time_horizon=TimeHorizon.DAYS,
        confidence=confidence,
    )


def test_decayed_score_empty() -> None:
    assert decayed_score([]) == 0.0


def test_recent_outweighs_stale() -> None:
    # Fresh strong positive vs. old strong negative -> net positive
    score = decayed_score([(_sig(0.9, 0.9, 1.0), 0.0), (_sig(-0.9, 0.9, 1.0), 30.0)])
    assert score > 0


def test_score_in_range() -> None:
    score = decayed_score([(_sig(0.8, 0.7, 0.9), 1.0)])
    assert -1.0 <= score <= 1.0


def test_target_weight_caps() -> None:
    p = SizingParams(max_position_pct=5.0)
    w = target_weight(1.0, daily_vol_pct=0.5, params=p)  # very low vol -> wants huge -> capped
    assert w == 5.0


def test_target_weight_below_min_is_zero() -> None:
    assert target_weight(0.05, daily_vol_pct=2.0) == 0.0


def test_lower_vol_bigger_size() -> None:
    hi = target_weight(0.5, daily_vol_pct=4.0)
    lo = target_weight(0.5, daily_vol_pct=2.0)
    assert lo > hi


def test_daily_volatility() -> None:
    assert daily_volatility_pct([100, 100, 100]) == 0.0
    assert daily_volatility_pct([100, 110, 100]) > 0
