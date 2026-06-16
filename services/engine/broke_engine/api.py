"""FastAPI surface for the engine (REST + a WebSocket stub).

Paper-first. Endpoints return stubbed/mock data in Phase 0-1 until the engine and
broker are wired (Phase 2). POST /orders returns a *proposed* order only — it never
executes (live execution requires the risk gate + human approval). See
docs/01-architecture/api-orchestration.md.
"""

from __future__ import annotations

from fastapi import FastAPI, WebSocket
from pydantic import BaseModel

from . import mockdata
from .config import settings

app = FastAPI(title="broke engine", version="0.0.1")


class OrderRequest(BaseModel):
    symbol: str
    side: str  # "buy" | "sell"
    qty: float
    order_type: str = "market"


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "mode": settings.trading_mode, "live": settings.is_live}


@app.get("/portfolio")
def portfolio() -> dict:
    return mockdata.PORTFOLIO


@app.get("/positions")
def positions() -> list[dict]:
    return mockdata.POSITIONS


@app.get("/orders")
def orders() -> list[dict]:
    return mockdata.ORDERS


@app.post("/orders")
def propose_order(order: OrderRequest) -> dict:
    """Return a PROPOSED order. Never executes — routes to the risk gate + approval."""
    return {
        "status": "proposed",
        "symbol": order.symbol,
        "side": order.side,
        "qty": order.qty,
        "order_type": order.order_type,
        "note": "proposed only; requires risk-gate pass + approval before execution",
    }


@app.get("/strategies")
def strategies() -> list[dict]:
    return mockdata.STRATEGIES


@app.get("/signals")
def signals() -> list[dict]:
    return mockdata.SIGNALS


@app.get("/digest/today")
def digest_today() -> dict:
    return mockdata.DIGEST


@app.get("/alerts")
def alerts() -> list[dict]:
    return mockdata.ALERTS


@app.websocket("/ws")
async def ws(websocket: WebSocket) -> None:
    """Stub: accepts, sends one hello frame, closes. Real streams (quotes/fills/pnl) land in Phase 3."""
    await websocket.accept()
    await websocket.send_json({"channel": "hello", "mode": settings.trading_mode})
    await websocket.close()
