"""Execution behind a stable interface — same engine code, swappable venue.

`SimulatedMatcher` is the paper/backtest venue: deterministic fills with slippage +
commission, and idempotent submission (resubmitting a client_order_id never double-fills).
Real brokers (Alpaca/IBKR) implement the same `ExecutionAdapter` later.
See docs/01-architecture/execution.md.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class Order:
    client_order_id: str  # idempotency key
    symbol: str
    side: str  # "buy" | "sell"
    qty: float
    order_type: str = "market"
    limit_price: float | None = None


@dataclass(frozen=True)
class Fill:
    client_order_id: str
    symbol: str
    side: str
    qty: float
    price: float
    commission: float
    slippage: float
    ts: datetime


class ExecutionAdapter(ABC):
    @abstractmethod
    def submit(self, order: Order, ref_price: float) -> Fill:
        raise NotImplementedError

    @abstractmethod
    def positions(self) -> dict[str, float]:
        raise NotImplementedError


class SimulatedMatcher(ExecutionAdapter):
    def __init__(self, slippage_bps: float = 2.0, commission_per_share: float = 0.0) -> None:
        self.slippage_bps = slippage_bps
        self.commission_per_share = commission_per_share
        self._fills: dict[str, Fill] = {}
        self._positions: dict[str, float] = {}

    def submit(self, order: Order, ref_price: float) -> Fill:
        # Idempotent: same client_order_id returns the original fill, no double-fill.
        if order.client_order_id in self._fills:
            return self._fills[order.client_order_id]
        if ref_price <= 0:
            raise ValueError("ref_price must be > 0")

        slip = ref_price * (self.slippage_bps / 10_000)
        if order.side == "buy":
            price = ref_price + slip  # pay up
        elif order.side == "sell":
            price = ref_price - slip  # receive less
        else:
            raise ValueError(f"bad side: {order.side!r}")

        commission = self.commission_per_share * order.qty
        fill = Fill(
            client_order_id=order.client_order_id,
            symbol=order.symbol,
            side=order.side,
            qty=order.qty,
            price=round(price, 4),
            commission=round(commission, 4),
            slippage=round(slip, 4),
            ts=datetime.now(timezone.utc),
        )
        signed = order.qty if order.side == "buy" else -order.qty
        self._positions[order.symbol] = self._positions.get(order.symbol, 0.0) + signed
        self._fills[order.client_order_id] = fill
        return fill

    def positions(self) -> dict[str, float]:
        return dict(self._positions)
