"""Autonomous paper-trading cycle.

One cycle: for each watchlist ticker, pull recent real news (Polygon), have Claude score it
(real reasoning), and if conviction clears the bar, size it (vol-scaled), pass it through the
risk gate, and fill it against real prices via the simulated matcher. Every step is logged as an
activity entry (the same shape the UI renders). Autopilot: no human approval (paper money).

HONEST: this demonstrates the agent operating end-to-end and produces REAL results (wins AND
losses). It is NOT a validated money-maker — see docs/05-research/edge-findings.md.
"""

from __future__ import annotations

import time
from datetime import datetime, timedelta, timezone

from ..data.polygon_news import fetch_news
from ..data.polygon_store import PolygonPointInTimeStore
from ..execution.adapter import Order, SimulatedMatcher
from ..llm import get_provider
from ..risk import AccountState, OrderIntent, RiskGate
from ..signals.scorer import score_news
from ..strategies.sizing import SizingParams, daily_volatility_pct, target_weight
from .portfolio import PaperPortfolio


def run_cycle(
    portfolio: PaperPortfolio,
    watchlist: list[str],
    *,
    provider=None,
    store=None,
    matcher: SimulatedMatcher | None = None,
    risk_gate: RiskGate | None = None,
    sizing: SizingParams | None = None,
    surprise_threshold: float = 0.5,
    min_notional: float = 500.0,
    news_days: int = 10,
    rate_sleep: float = 13.0,
) -> list[dict]:
    provider = provider or get_provider()
    store = store or PolygonPointInTimeStore()
    matcher = matcher or SimulatedMatcher()
    risk_gate = risk_gate or RiskGate()
    sizing = sizing or SizingParams()
    now = datetime.now(timezone.utc)
    ts = now.isoformat(timespec="minutes")
    cycle_id = now.strftime("%Y%m%d%H%M%S")

    activity: list[dict] = []
    prices: dict[str, float] = {}
    scored: dict[str, tuple] = {}  # ticker -> (signal, vol)

    for tk in watchlist:
        bars = store.get_bars(tk, now - timedelta(days=45), now, as_of=now)
        time.sleep(rate_sleep)
        if not bars:
            continue
        prices[tk] = bars[-1].close
        vol = daily_volatility_pct([b.close for b in bars[-20:]]) or 2.0
        news = fetch_news(tk, now - timedelta(days=news_days), now, limit=3)
        time.sleep(rate_sleep)
        if not news:
            continue
        headline = news[-1][1]
        sig = score_news(provider, tk, headline)
        scored[tk] = (sig, vol)
        activity.append({
            "ts": ts, "type": "signal", "symbol": tk,
            "action": f"Scored: {headline[:90]}",
            "reasoning": sig.rationale or f"sentiment {sig.sentiment:+.2f}, surprise {sig.surprise:.2f}",
            "outcome": "No trade",
        })

    equity = portfolio.equity(prices) or 100_000.0

    for tk, (sig, vol) in scored.items():
        if sig.surprise < surprise_threshold:
            continue
        score = sig.sentiment * sig.surprise
        tw = target_weight(score, vol, sizing)
        if abs(tw) < 0.1:
            continue
        price = prices[tk]
        delta = (tw / 100.0 * equity) / price - portfolio.positions.get(tk, 0.0)
        notional = abs(delta) * price
        if notional < min_notional:
            continue
        side = "buy" if delta > 0 else "sell"
        gross = sum(abs(q) * prices.get(s, 0.0) for s, q in portfolio.positions.items())
        decision = risk_gate.check(
            OrderIntent(tk, side, notional),
            AccountState(equity=equity, gross_exposure=gross, day_pnl=0.0, new_positions_this_week=0),
        )
        if not decision.approved:
            activity.append({
                "ts": ts, "type": "rejected", "symbol": tk,
                "action": f"Risk gate blocked {side.upper()} {tk}",
                "reasoning": "; ".join(decision.reasons), "outcome": "Blocked",
            })
            continue
        fill = matcher.submit(Order(f"{cycle_id}-{tk}", tk, side, abs(delta)), ref_price=price)
        portfolio.apply_fill(tk, side, fill.qty, fill.price)
        verb = "Bought" if side == "buy" else "Sold"
        activity.append({
            "ts": ts, "type": "filled", "symbol": tk,
            "action": f"{verb} {round(fill.qty, 1)} {tk} @ ${round(fill.price, 2)} (paper)",
            "reasoning": f"{sig.rationale} (surprise {sig.surprise:.2f}, sentiment {sig.sentiment:+.2f}); "
                         f"sized {tw:+.1f}% vol-scaled; cleared the risk gate.",
            "outcome": "Open",
        })

    portfolio.equity_history.append({"ts": ts, "equity": round(portfolio.equity(prices), 2)})
    return activity
