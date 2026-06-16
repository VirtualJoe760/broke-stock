"""FastAPI surface for the engine (REST now; WebSocket in Phase 3).

Paper-first. Endpoints return stubbed/mock data in Phase 0–1 until the engine and
broker are wired (Phase 2). See docs/01-architecture/api-orchestration.md.
"""

from __future__ import annotations

from fastapi import FastAPI

from .config import settings

app = FastAPI(title="broke engine", version="0.0.1")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "mode": settings.trading_mode, "live": settings.is_live}


@app.get("/portfolio")
def portfolio() -> dict:
    """Phase 0 stub — mock paper portfolio until Phase 2 wires the engine/broker."""
    return {
        "mode": settings.trading_mode,
        "equity": 0.0,
        "buying_power": 0.0,
        "day_pnl": 0.0,
        "positions": [],
        "stub": True,
    }
