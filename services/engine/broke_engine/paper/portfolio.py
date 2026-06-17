"""A paper portfolio (play money). Persisted as JSON between cycles."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class PaperPortfolio:
    cash: float = 100_000.0
    positions: dict[str, float] = field(default_factory=dict)  # symbol -> shares
    equity_history: list[dict] = field(default_factory=list)  # [{ts, equity}]

    def equity(self, prices: dict[str, float]) -> float:
        v = self.cash
        for sym, qty in self.positions.items():
            v += qty * prices.get(sym, 0.0)
        return v

    def apply_fill(self, symbol: str, side: str, qty: float, price: float) -> None:
        signed = qty if side == "buy" else -qty
        self.cash -= signed * price
        new_qty = self.positions.get(symbol, 0.0) + signed
        if abs(new_qty) < 1e-9:
            self.positions.pop(symbol, None)
        else:
            self.positions[symbol] = new_qty

    def to_dict(self) -> dict:
        return {
            "cash": round(self.cash, 2),
            "positions": {k: round(v, 4) for k, v in self.positions.items()},
            "equity_history": self.equity_history,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "PaperPortfolio":
        return cls(
            cash=float(d.get("cash", 100_000.0)),
            positions={k: float(v) for k, v in d.get("positions", {}).items()},
            equity_history=list(d.get("equity_history", [])),
        )
