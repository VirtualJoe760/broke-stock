"""Signal scoring: the schema Claude conforms to (see models.py)."""

from .models import (
    EventType,
    Magnitude,
    Signal,
    TimeHorizon,
    signal_json_schema,
)

__all__ = ["Signal", "EventType", "Magnitude", "TimeHorizon", "signal_json_schema"]
