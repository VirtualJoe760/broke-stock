"""The wheel — backtest/event-study harness (skeleton).

Sells cash-secured puts; on assignment, holds shares and sells covered calls; repeats.
Runs end-to-end over a PointInTimeStore and produces metrics.

HONEST CAVEAT: this is a runnable SKELETON, not a validated backtest. Option premiums
here are crude proxies (a fixed % of notional per cycle) — there is no real option chain,
IV, or Greeks yet. It exists to prove the pipeline executes offline and emits the right
metrics; it is pre-L2 on the validation ladder. Real option data replaces the proxy before
any result is trusted. See docs/04-strategies/003-the-wheel-options-income.md and
docs/05-research/validation-methodology.md.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from ..data.store import PointInTimeStore


@dataclass
class WheelParams:
    put_otm_pct: float = 0.05  # cash-secured put strike this far below price
    call_otm_pct: float = 0.05  # covered call strike this far above price
    premium_pct: float = 0.015  # PROXY premium per cycle (~1.5% of strike notional)
    cycle_days: int = 21  # ~1 month of trading days per option cycle
    contracts: int = 1  # 1 contract = 100 shares
    starting_cash: float = 100_000.0


@dataclass
class WheelResult:
    symbol: str
    start: datetime
    end: datetime
    cycles: int
    assignments: int
    premium_collected: float
    assignment_loss: float  # sum of underwater amount at assignment (proxy)
    final_equity: float
    total_return_pct: float
    max_drawdown_pct: float
    note: str = "skeleton: premiums are proxies, not real option pricing (pre-L2)"


class WheelBacktest:
    def __init__(self, store: PointInTimeStore, params: WheelParams | None = None) -> None:
        self.store = store
        self.p = params or WheelParams()

    def run(self, symbol: str, start: datetime, end: datetime) -> WheelResult:
        p = self.p
        shares_per_contract = 100 * p.contracts
        bars = self.store.get_bars(symbol, start, end, as_of=end)
        if len(bars) < p.cycle_days + 1:
            raise ValueError("not enough bars for even one cycle")

        cash = p.starting_cash
        shares = 0
        premium_collected = 0.0
        assignment_loss = 0.0
        cycles = 0
        assignments = 0
        equity_curve: list[float] = []

        i = 0
        while i < len(bars) - 1:
            entry = bars[i]
            j = min(i + p.cycle_days, len(bars) - 1)
            expiry = bars[j]
            cycles += 1

            if shares == 0:
                # Cash-secured put
                strike = entry.close * (1 - p.put_otm_pct)
                premium = p.premium_pct * strike * shares_per_contract
                cash += premium
                premium_collected += premium
                if expiry.close < strike:  # assigned
                    cash -= strike * shares_per_contract
                    shares += shares_per_contract
                    assignments += 1
                    assignment_loss += max(0.0, strike - expiry.close) * shares_per_contract
            else:
                # Covered call
                strike = entry.close * (1 + p.call_otm_pct)
                premium = p.premium_pct * strike * shares_per_contract
                cash += premium
                premium_collected += premium
                if expiry.close >= strike:  # called away
                    cash += strike * shares_per_contract
                    shares -= shares_per_contract

            equity = cash + shares * expiry.close
            equity_curve.append(equity)
            i = j

        final_equity = cash + shares * bars[-1].close
        total_return_pct = (final_equity / p.starting_cash - 1) * 100

        peak = float("-inf")
        mdd = 0.0
        for eq in equity_curve:
            peak = max(peak, eq)
            if peak > 0:
                mdd = max(mdd, (peak - eq) / peak)

        return WheelResult(
            symbol=symbol,
            start=start,
            end=end,
            cycles=cycles,
            assignments=assignments,
            premium_collected=round(premium_collected, 2),
            assignment_loss=round(assignment_loss, 2),
            final_equity=round(final_equity, 2),
            total_return_pct=round(total_return_pct, 2),
            max_drawdown_pct=round(mdd * 100, 2),
        )
