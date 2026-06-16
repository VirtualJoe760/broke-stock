"""Event-study pipeline logic — tested with a fake provider (no Anthropic call)."""

from datetime import datetime, timezone
from typing import Any

from broke_engine.data.store import MockPointInTimeStore
from broke_engine.llm.provider import LLMProvider
from broke_engine.research import NewsEvent, run_event_study


class QueueProvider(LLMProvider):
    """Returns canned signal dicts in order — lets us test the join/metric without an LLM."""

    def __init__(self, signals: list[dict[str, Any]]) -> None:
        self._q = list(signals)

    def complete(self, system: str, user: str, *, schema: dict[str, Any] | None = None) -> Any:
        return self._q.pop(0)


def _sig(sentiment: float, surprise: float) -> dict[str, Any]:
    return {
        "ticker": "X",
        "event_type": "earnings",
        "sentiment": sentiment,
        "surprise": surprise,
        "magnitude": "moderate",
        "time_horizon": "days",
        "confidence": 0.8,
    }


def test_event_study_runs_and_buckets() -> None:
    store = MockPointInTimeStore()
    events = [
        NewsEvent(datetime(2024, 2, 1, tzinfo=timezone.utc), "AAA", "good news"),
        NewsEvent(datetime(2024, 2, 1, tzinfo=timezone.utc), "BBB", "bad news"),
    ]
    provider = QueueProvider([_sig(0.8, 0.9), _sig(-0.8, 0.9)])

    result = run_event_study(events, provider, store, horizon_days=5)

    assert result.n == 2
    assert isinstance(result.long_short_spread_pct, float)
    # both were high-surprise; one long, one short -> spread is long_avg - short_avg
    assert result.long_short_spread_pct == round(
        result.long_avg_return_pct - result.short_avg_return_pct, 3
    )
