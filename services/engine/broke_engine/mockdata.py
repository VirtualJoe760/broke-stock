"""Mock/stub data for the API in paper mode (no broker, no keys).

Replaced by real engine/broker state in Phase 2. Stdlib only so it imports anywhere.
"""

from __future__ import annotations

MODE = "paper"

PORTFOLIO = {
    "mode": MODE,
    "equity": 104820.0,
    "buying_power": 38500.0,
    "day_pnl": 1240.0,
    "total_pnl": 4820.0,
    "stub": True,
}

POSITIONS = [
    {"symbol": "NVDA", "qty": 120, "avg_price": 163.70, "last": 184.20, "unrealized_pnl": 2460.0, "ai_confidence": 0.81},
    {"symbol": "AVGO", "qty": 60, "avg_price": 232.40, "last": 242.10, "unrealized_pnl": 580.0, "ai_confidence": 0.64},
    {"symbol": "AAPL", "qty": 90, "avg_price": 218.00, "last": 214.55, "unrealized_pnl": -310.0, "ai_confidence": 0.48},
]

ORDERS = [
    {"id": "o-1001", "symbol": "NVDA", "side": "buy", "qty": 120, "type": "market", "status": "filled"},
]

STRATEGIES = [
    {"id": "001", "name": "LEAPS + catalyst swing", "validation_level": "L0"},
    {"id": "002", "name": "Fundamentals, beat the benchmark", "validation_level": "L0"},
    {"id": "003", "name": "The wheel (options income)", "validation_level": "L0"},
]

SIGNALS = [
    {"ticker": "NVDA", "event_type": "guidance_raise", "sentiment": 0.7, "surprise": 0.81, "confidence": 0.72},
    {"ticker": "MU", "event_type": "earnings", "sentiment": 0.6, "surprise": 0.74, "confidence": 0.66},
]

DIGEST = {
    "date": "2026-06-16",
    "confidence": 0.72,
    "brief": "Overnight, semiconductor names rallied on stronger Taiwan export data, lifting the two largest holdings. Futures point modestly higher; a 10:00 ET inflation print is the day's main risk.",
}

ALERTS = [
    {"id": "a-1", "tier": "notice", "message": "NVDA target approaching", "channel": "telegram"},
]
