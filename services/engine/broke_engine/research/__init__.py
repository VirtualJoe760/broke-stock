"""Research harnesses — the L2 event study (does a signal predict forward returns?)."""

from .event_study import (
    EventOutcome,
    EventStudyResult,
    NewsEvent,
    forward_return_pct,
    run_event_study,
)

__all__ = [
    "NewsEvent",
    "EventOutcome",
    "EventStudyResult",
    "run_event_study",
    "forward_return_pct",
]
