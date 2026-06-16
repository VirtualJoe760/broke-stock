# Engine & parity

The core commitment ([ADR-001](../00-overview/decisions-log.md)): one event-driven engine, one code path, three modes.

## Principle

The same strategy code consumes one event-stream abstraction (bars, quotes, trades, order-book deltas). Mode is determined by three swappable parts:

| Part | Backtest | Paper | Live |
|---|---|---|---|
| Clock | simulated (fast replay) | wall clock | wall clock |
| Data source | historical (DuckDB/Parquet) | live feed | live feed |
| Execution venue | simulated matcher | broker paper API | broker live API |

## Engine choice

NautilusTrader (Rust core, Python API) — built for backtest↔live parity, realistic order matching, latency/slippage modeling. Fallback: a custom event-loop engine preserving the same abstraction.

## Strategy interface contract

Every strategy is a class with a fixed lifecycle, identical across modes:

- `on_start()` — declare data subscriptions, load validated parameters (frozen for live).
- `on_event(event)` — receive bars/quotes/trades/signals; emit orders via the order API.
- `on_order_filled(fill)` / `on_position_changed(...)` — react to executions.
- `on_stop()` — flush state.

Strategies emit *intents* (target positions / orders); they never call a broker directly — the [risk gate](risk-gate.md) and [execution](execution.md) layers sit between intent and venue.

## Matching-engine realism (backtest/paper)

To keep backtests honest, the simulated matcher models: fills against the book, slippage, spread, commissions, and configurable latency. For options, it models spread and (where possible) assignment. Defaults are conservative — an over-optimistic matcher is how backtests lie.

## Determinism & replay

Backtests are deterministic: same inputs + same params → same result. Combined with the event-sourced log ([persistence & events](persistence-and-events.md)), any run can be replayed exactly — essential for debugging and for the [validation ladder](../05-research/validation-methodology.md).

## Data subscriptions

A strategy declares what it needs (symbols, bar sizes, quote/trade streams, option chains). The engine wires those to the active data source per mode, so the strategy is agnostic to whether data is historical or live.

## Open questions

- Exact NautilusTrader version pinning + multi-arch native build ([deployment](../08-deployment/deployment-and-portability.md)).
- How options/Greeks events are represented in the stream.
