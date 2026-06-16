# Trader dashboard (cockpit)

## Purpose

The "monitor & act" surface. Dense, real-time, decisive.

## Features (priority)

- **MODE banner** — unmissable PAPER / LIVE (color + confirmation on live orders). [MVP]
- Portfolio header (equity, day/total P&L, buying power). [MVP]
- Positions blotter with per-position **AI confidence** + link to thesis. [MVP]
- Order ticket + OMS (market/limit/stop/bracket). [MVP]
- **AI trade proposal** with approve/reject + autopilot toggle. [MVP]
- Risk panel + **kill switch**. [MVP]
- Equity curve, watchlist. [MVP]
- Depth/DOM, performance analytics, system-health strip. [Phase 2]

## Options view (from digest 001)

Strike ladder, Greeks, theta-decay view, macro gate (VIX, breadth, credit spreads) — for the options strategy classes ([ADR-005](../00-overview/decisions-log.md), [strategy 001](../04-strategies/001-leaps-catalyst-swing.md), [003 the wheel](../04-strategies/003-the-wheel-options-income.md)).

## Component inventory + data contracts

| Component | Source |
|---|---|
| Portfolio header / equity curve | `GET /portfolio` + `pnl` WS |
| Positions blotter | `GET /positions` + `positions`/`pnl` WS |
| Order ticket / OMS | `POST /orders`, `DELETE /orders/{id}`, `orders` WS |
| AI proposal | `signals` WS → proposed order; approve = `POST /orders` confirm |
| Risk panel / kill switch | `GET /account` limits + risk-gate state; kill = risk endpoint |
| Charts | price data via API; TradingView Lightweight Charts |

## Approval & safety

Live orders flow through the approval gate ([risk gate](../01-architecture/risk-gate.md), [ADR-004](../00-overview/decisions-log.md)); the MODE banner and a live-order confirmation make PAPER/LIVE impossible to confuse.

## Tech

Next.js + React + TS on Vercel; **TradingView Lightweight Charts**; live state over WebSocket from the [API](../01-architecture/api-orchestration.md).

## Reference

Mockup built during the design phase (mode banner, metrics, equity curve, blotter, AI proposal, order ticket, risk/kill switch).
