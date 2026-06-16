"""The wheel harness runs offline over mock data and emits sane metrics."""

from datetime import datetime, timezone

from broke_engine.data.store import MockPointInTimeStore
from broke_engine.strategies import WheelBacktest, WheelResult


def test_wheel_runs_and_produces_metrics() -> None:
    store = MockPointInTimeStore()
    start = datetime(2024, 1, 1, tzinfo=timezone.utc)
    end = datetime(2024, 12, 31, tzinfo=timezone.utc)

    result = WheelBacktest(store).run("WHEEL", start, end)

    assert isinstance(result, WheelResult)
    assert result.cycles > 0
    assert result.premium_collected > 0
    assert result.final_equity > 0
    assert 0 <= result.max_drawdown_pct <= 100
