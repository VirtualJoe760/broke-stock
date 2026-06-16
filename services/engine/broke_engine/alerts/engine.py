"""Evaluate alert rules against account/market state -> fired alerts.

Pure function, stdlib only. `state` is a dict with optional keys:
  positions: [{symbol, last}], equity: float, day_pnl: float, signals: [{ticker, confidence}]
"""

from __future__ import annotations

from typing import Any

from .models import Alert, AlertRule, AlertType, Tier


def evaluate(rules: list[AlertRule], state: dict[str, Any]) -> list[Alert]:
    alerts: list[Alert] = []
    positions = {p["symbol"]: p for p in state.get("positions", [])}
    equity = float(state.get("equity", 0.0))
    day_pnl = float(state.get("day_pnl", 0.0))

    for r in rules:
        if r.type == AlertType.PRICE_TARGET and r.symbol in positions:
            if positions[r.symbol]["last"] >= r.threshold:
                alerts.append(Alert(Tier.NOTICE, r.type, f"{r.symbol} reached target {r.threshold}", r.symbol))

        elif r.type == AlertType.STOP and r.symbol in positions:
            if positions[r.symbol]["last"] <= r.threshold:
                alerts.append(Alert(Tier.URGENT, r.type, f"{r.symbol} hit stop {r.threshold}", r.symbol))

        elif r.type == AlertType.DAILY_LOSS:
            if equity > 0 and day_pnl <= -abs(r.threshold / 100 * equity):
                alerts.append(Alert(Tier.CRITICAL, r.type, f"daily loss limit {r.threshold}% breached"))

        elif r.type == AlertType.SIGNAL:
            for s in state.get("signals", []):
                if s.get("confidence", 0) >= r.threshold and (r.symbol is None or s.get("ticker") == r.symbol):
                    alerts.append(Alert(Tier.NOTICE, r.type, f"high-confidence signal on {s.get('ticker')}", s.get("ticker")))

    return alerts
