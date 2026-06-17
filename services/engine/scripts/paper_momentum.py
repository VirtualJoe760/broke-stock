"""Run one autonomous MOMENTUM paper-trading cycle (real prices, no LLM) and write the UI feed.

Trades on real price action so the /activity feed shows actual fills + a moving P&L.
EXPLORATION strategy on play money — not a validated edge. Requires POLYGON_API_KEY.
Run from services/engine.
"""

from __future__ import annotations

import json
from pathlib import Path

from broke_engine.paper import PaperPortfolio, run_momentum_cycle

WATCHLIST = ["NVDA", "MSFT", "AMD", "MU", "AAPL", "META", "AMZN", "GOOGL"]
WEB_LIB = Path(__file__).resolve().parents[3] / "apps" / "web" / "lib"
ACT = WEB_LIB / "live-activity.json"
PORT = WEB_LIB / "live-portfolio.json"


def main() -> None:
    portfolio = PaperPortfolio.from_dict(json.loads(PORT.read_text())) if PORT.exists() else PaperPortfolio()
    existing = json.loads(ACT.read_text()) if ACT.exists() else []

    new_activity = run_momentum_cycle(portfolio, WATCHLIST)
    print(f"cycle produced {len(new_activity)} activity entries", flush=True)

    WEB_LIB.mkdir(parents=True, exist_ok=True)
    ACT.write_text(json.dumps((new_activity + existing)[:50], indent=1))
    PORT.write_text(json.dumps(portfolio.to_dict(), indent=1))

    eq = portfolio.equity_history[-1]["equity"] if portfolio.equity_history else None
    print(f"portfolio equity: {eq}  positions: {portfolio.positions}", flush=True)


if __name__ == "__main__":
    main()
