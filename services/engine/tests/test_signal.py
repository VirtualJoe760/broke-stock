"""Signal validation + LLM-JSON parsing."""

import pytest

from broke_engine.signals import EventType, Signal, signal_json_schema


def test_valid_signal() -> None:
    s = Signal.from_dict(
        {
            "ticker": "NVDA",
            "event_type": "guidance_raise",
            "sentiment": 0.7,
            "surprise": 0.81,
            "magnitude": "major",
            "time_horizon": "weeks",
            "confidence": 0.72,
            "rationale": "supply-chain read-through not yet priced in",
        }
    )
    assert s.ticker == "NVDA"
    assert s.event_type is EventType.GUIDANCE_RAISE


def test_out_of_range_rejected() -> None:
    with pytest.raises(ValueError):
        Signal(
            ticker="NVDA",
            event_type=EventType.OTHER,
            sentiment=1.5,  # invalid
            surprise=0.1,
            magnitude="minor",  # type: ignore[arg-type]
            time_horizon="days",  # type: ignore[arg-type]
            confidence=0.5,
            rationale="",
        )


def test_json_schema_has_required_fields() -> None:
    schema = signal_json_schema()
    for field in ("ticker", "event_type", "sentiment", "surprise", "confidence"):
        assert field in schema["required"]
