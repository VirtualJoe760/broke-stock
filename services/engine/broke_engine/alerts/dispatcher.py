"""Dispatch interface. Default NoopDispatcher records would-be sends — NO real network send.

Real channels (Telegram/SMS/spoken/outbound-call) implement AlertDispatcher later, behind
the same interface. See docs/03-voice-and-alerts/alerts-and-notifications.md.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from .models import Alert


class AlertDispatcher(ABC):
    @abstractmethod
    def dispatch(self, alert: Alert) -> None:
        raise NotImplementedError


class NoopDispatcher(AlertDispatcher):
    """Records what *would* be sent. Sends nothing — safe for paper/mock and tests."""

    def __init__(self) -> None:
        self.sent: list[Alert] = []

    def dispatch(self, alert: Alert) -> None:
        self.sent.append(alert)
