"""Signal scoring: the schema Claude conforms to (see models.py)."""

from .models import (
    EventType,
    Magnitude,
    Signal,
    TimeHorizon,
    signal_json_schema,
)
from .scorer import score_news

__all__ = ["Signal", "EventType", "Magnitude", "TimeHorizon", "signal_json_schema", "score_news"]
