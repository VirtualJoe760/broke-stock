"""Risk gate — hard, code-enforced limits between a proposed order and execution.

Never LLM. In autopilot this is the only thing between a hallucination and a loss.
See docs/01-architecture/risk-gate.md.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class RiskLimits:
    max_position_pct: float = 5.0  # max single position as % of equity
    max_gross_exposure_pct: float = 60.0
    daily_loss_limit_pct: float = 3.0  # trips the kill switch
    max_new_positions_per_week: int = 3
    allow_options: bool = False  # autonomous agent: options off by default


@dataclass
class OrderIntent:
    symbol: str
    side: str  # "buy" | "sell"
    notional: float  # dollar value of the order
    is_option: bool = False


@dataclass
class AccountState:
    equity: float
    gross_exposure: float  # current gross dollar exposure
    day_pnl: float  # today's realized + unrealized P&L (dollars)
    new_positions_this_week: int = 0


@dataclass
class RiskDecision:
    approved: bool
    kill_switch: bool
    reasons: list[str] = field(default_factory=list)


class RiskGate:
    def __init__(self, limits: RiskLimits | None = None) -> None:
        self.limits = limits or RiskLimits()

    def check(self, intent: OrderIntent, account: AccountState) -> RiskDecision:
        lim = self.limits
        reasons: list[str] = []

        if account.equity <= 0:
            return RiskDecision(False, kill_switch=True, reasons=["equity <= 0"])

        # Daily-loss kill switch (independent of this order)
        kill = account.day_pnl <= -abs(lim.daily_loss_limit_pct / 100 * account.equity)
        if kill:
            reasons.append("daily loss limit breached -> kill switch")

        if intent.is_option and not lim.allow_options:
            reasons.append("options not allowed for this account")

        pos_pct = intent.notional / account.equity * 100
        if pos_pct > lim.max_position_pct:
            reasons.append(
                f"position {pos_pct:.1f}% exceeds max {lim.max_position_pct:.1f}%"
            )

        # Buys add exposure; sells reduce it
        added = intent.notional if intent.side == "buy" else 0.0
        gross_pct = (account.gross_exposure + added) / account.equity * 100
        if gross_pct > lim.max_gross_exposure_pct:
            reasons.append(
                f"gross exposure {gross_pct:.1f}% exceeds max {lim.max_gross_exposure_pct:.1f}%"
            )

        if intent.side == "buy" and account.new_positions_this_week >= lim.max_new_positions_per_week:
            reasons.append("weekly new-position cap reached")

        approved = not reasons and not kill
        return RiskDecision(approved=approved, kill_switch=kill, reasons=reasons or ["ok"])
