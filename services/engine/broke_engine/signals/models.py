"""The signal schema — Claude turns text into one of these (structured output).

`surprise` (deviation from what's already priced in) is the alpha-bearing field, not
raw sentiment. See docs/01-architecture/signal-layer.md. Implemented with the stdlib so
it validates offline; the LLM tool emits JSON conforming to `signal_json_schema()`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class EventType(str, Enum):
    GUIDANCE_RAISE = "guidance_raise"
    GUIDANCE_CUT = "guidance_cut"
    UPGRADE = "upgrade"
    DOWNGRADE = "downgrade"
    MNA = "mna"
    LITIGATION = "litigation"
    EARNINGS = "earnings"
    MACRO = "macro"
    OTHER = "other"


class Magnitude(str, Enum):
    MINOR = "minor"
    MODERATE = "moderate"
    MAJOR = "major"


class TimeHorizon(str, Enum):
    INTRADAY = "intraday"
    DAYS = "days"
    WEEKS = "weeks"


def _check_range(name: str, value: float, lo: float, hi: float) -> None:
    if not lo <= value <= hi:
        raise ValueError(f"{name} must be in [{lo}, {hi}], got {value!r}")


@dataclass(frozen=True)
class Signal:
    ticker: str
    event_type: EventType
    sentiment: float  # -1.0 .. 1.0
    surprise: float  # 0.0 .. 1.0  (alpha-bearing)
    magnitude: Magnitude
    time_horizon: TimeHorizon
    confidence: float  # 0.0 .. 1.0
    rationale: str = ""  # optional; not in the required JSON-schema fields

    def __post_init__(self) -> None:
        if not self.ticker:
            raise ValueError("ticker is required")
        _check_range("sentiment", self.sentiment, -1.0, 1.0)
        _check_range("surprise", self.surprise, 0.0, 1.0)
        _check_range("confidence", self.confidence, 0.0, 1.0)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Signal":
        """Parse an LLM JSON object (string enums coerced) into a validated Signal."""
        return cls(
            ticker=d["ticker"],
            event_type=EventType(d["event_type"]),
            sentiment=float(d["sentiment"]),
            surprise=float(d["surprise"]),
            magnitude=Magnitude(d["magnitude"]),
            time_horizon=TimeHorizon(d["time_horizon"]),
            confidence=float(d["confidence"]),
            rationale=d.get("rationale", ""),
        )


def signal_json_schema() -> dict[str, Any]:
    """JSON schema for the structured-output tool the LLM must call."""
    return {
        "type": "object",
        "properties": {
            "ticker": {"type": "string"},
            "event_type": {"type": "string", "enum": [e.value for e in EventType]},
            "sentiment": {"type": "number", "minimum": -1, "maximum": 1},
            "surprise": {"type": "number", "minimum": 0, "maximum": 1},
            "magnitude": {"type": "string", "enum": [m.value for m in Magnitude]},
            "time_horizon": {"type": "string", "enum": [h.value for h in TimeHorizon]},
            "confidence": {"type": "number", "minimum": 0, "maximum": 1},
            "rationale": {"type": "string"},
        },
        "required": [
            "ticker",
            "event_type",
            "sentiment",
            "surprise",
            "magnitude",
            "time_horizon",
            "confidence",
        ],
    }
