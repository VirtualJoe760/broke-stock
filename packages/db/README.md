# broke db

Drizzle ORM schema + migrations for app state on Postgres/Neon ([persistence & events](../../docs/01-architecture/persistence-and-events.md)).

## Tables (`src/schema.ts`)

- `accounts` — mode (paper/live), broker, equity, buying power
- `strategies` — name, **validation_level** (L0–L5, gates capital), params (jsonb), frozen
- `orders` — account, strategy, symbol, side, type, qty, status, client_order_id (idempotent), correlation_id
- `positions` — account, symbol, qty, avg_price, unrealized_pnl
- `fills` — order, ts, qty, price, fees, slippage
- `audit` — actor (agent/human/system), action, before/after, correlation_id

Time-series ticks live in QuestDB/DuckDB, **not** here.

## Usage

```
DATABASE_URL=... pnpm generate   # create SQL migrations from schema
DATABASE_URL=... pnpm migrate    # apply them
```

> Migrations are generated against a real `DATABASE_URL` (Neon) when you're set up — not run during the offline build.
