# Persistence & events

## Two stores, different jobs

- **App state (Postgres / Neon + Drizzle):** accounts, orders, positions, P&L, audit trail, strategy config.
- **Time-series:** DuckDB/Parquet (research) and QuestDB (live ticks). Don't force ticks into Postgres ([data & ingestion](data-and-ingestion.md)).

## Event backbone

- **Phase 1:** Redis Streams (simple, replayable).
- **Scale:** NATS or Redpanda/Kafka for an event-sourced, replayable log.
- Every tick/order/fill/signal/alert is an **immutable event** → deterministic replay + free auditability ([engine & parity](engine-and-parity.md)).

## Event model (draft)

`event_id, ts, type, payload, source, correlation_id` — where `type` ∈ {market_data, signal, order_intent, order_submitted, fill, position_change, alert, decision}. `correlation_id` threads a signal → intent → order → fill so any trade is fully reconstructable.

## App schema (draft, Drizzle)

- `accounts` — id, mode (paper/live), broker, balances
- `strategies` — id, name, validation_level, params (frozen for live)
- `orders` — id, account_id, symbol, side, type, qty, status, client_order_id, correlation_id
- `positions` — account_id, symbol, qty, avg_price, unrealized_pnl
- `fills` — order_id, ts, qty, price, fees, slippage
- `audit` — ts, actor (agent/human), action, before/after, correlation_id

## Audit (also a compliance control)

Every AI decision, signal, order, alert, and generated audio is logged and reconstructable — required for debugging and for [compliance](../06-compliance/regulatory-and-risk.md).

## Retention & persistence

- App DB: durable (Neon).
- Snapshots/data: object storage or mounted volume so they survive container restarts ([deployment](../08-deployment/deployment-and-portability.md)).
- Define retention windows per data class (ticks vs. audit vs. snapshots).

## Open questions

- Event store choice for Phase 1 (Redis Streams) vs. when to graduate to NATS/Redpanda.
- Exact retention policy per class.
