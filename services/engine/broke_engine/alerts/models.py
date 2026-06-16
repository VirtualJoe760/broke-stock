"""Alert rules + fired alerts. See docs/03-voice-and-alerts/alerts-and-notifications.md."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AlertType(str, Enum):
    PRICE_TARGET = "price_target"
    STOP = "stop"
    DAILY_LOSS = "daily_loss"
    SIGNAL = "signal"  # high-confidence signal on a holding/watchlist


class Tier(str, Enum):
    INFO = "info"
    NOTICE = "notice"
    URGENT = "urgent"
    CRITICAL = "critical"


@dataclass(frozen=True)
class AlertRule:
    type: AlertType
    threshold: float  # price (target/stop), % of equity (daily_loss), or confidence (signal)
    symbol: str | None = None  # None = any (for signal rules)


@dataclass(frozen=True)
class Alert:
    tier: Tier
    type: AlertType
    message: str
    symbol: str | None = None
