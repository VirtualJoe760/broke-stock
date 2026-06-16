# Execution

## Responsibility

Translate approved, risk-checked target positions into orders at a venue, behind a stable interface so the engine doesn't care whether it's simulated or live ([engine & parity](engine-and-parity.md)).

## Venues

- **Simulated matcher** — backtest/paper (realistic fills/slippage/spread).
- **Alpaca** — paper + live; cleanest API; default.
- **Interactive Brokers** — breadth, options.

## Adapter interface

One interface, multiple implementations:

- `submit(order)` / `cancel(order_id)` / `replace(...)`
- `get_positions()` / `get_orders()` / `get_account()`
- streams: `on_fill`, `on_order_update`

Swapping paper ↔ live ↔ sim is a config change, not a code change.

## Order handling

- **Bracket / OCO** orders so every entry ships with a stop and target baked in at submit time.
- **Idempotent submission** (client order IDs) to survive retries/restarts without duplicate orders.
- **Fill reconciliation** — reconcile broker fills against intended orders; surface partial fills and rejects; update positions/P&L in the [event store](persistence-and-events.md).

## PAPER / LIVE guardrails at the boundary

- Mode is explicit and loud; live submission requires the human-approval gate ([risk gate](risk-gate.md)).
- **Least-privilege credentials** — trade-only broker keys; no withdrawal/transfer scope ([compliance](../06-compliance/regulatory-and-risk.md)).
- A fresh deployment defaults to paper ([distribution](../08-deployment/distribution.md)).

## Open questions

- Options order-type coverage per venue (multi-leg, assignment handling).
- Reconciliation cadence and handling of out-of-band fills (e.g. manual trades).
