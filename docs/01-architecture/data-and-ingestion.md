# Data & ingestion

## Responsibility

Acquire and store market + text data so it can drive both backtests and live trading, with **point-in-time** integrity.

## Sources (by fidelity tier)

- **Equity / price:** Alpaca (free IEX, MVP) → Polygon (flat-rate real-time) → Databento (tick + L2/MBO).
- **Options:** chains + Greeks (Yahoo free / compute locally → FMP / premium).
- **Text / research:** news APIs (Alpaca news WebSocket, Benzinga, Polygon), SEC EDGAR filings, earnings-call transcripts, Perplexity for agent-driven research, social/alt-data.

## Storage

- **Research / backtest:** Parquet + DuckDB (columnar, fast, file-based).
- **Live ticks:** QuestDB (high-ingest append-only).
- **App state:** Postgres/Neon ([persistence & events](persistence-and-events.md)) — not for ticks.

## Point-in-time integrity (non-negotiable)

Every record carries an **ingest timestamp** = when the data was actually known. Backtests may only read data whose ingest time ≤ the simulated clock. This is what prevents lookahead bias and is the foundation the [validation methodology](../05-research/validation-methodology.md) depends on.

## Snapshot + diff (change detection)

Each scheduled run saves a daily snapshot (positions, prices, option chains, Greeks). The alert engine **diffs today vs. yesterday** to detect new strikes/expiries, large IV moves, or target/stop crossings (reference design: [digest 001](../05-research/video-digests/001-brandon-claude-robinhood.md)). Snapshots also feed reproducibility.

## Core schemas (draft)

- **bar** — `symbol, ts, open, high, low, close, volume, ingest_ts`
- **quote/trade** — `symbol, ts, bid/ask or price, size, ingest_ts`
- **option_contract** — `underlying, expiry, strike, type, bid, ask, iv, delta, theta, gamma, vega, oi, ingest_ts`
- **news_item** — `id, ts, source, tickers[], headline, body, url, ingest_ts`

## Backfill & survivorship

Historical backfill must **include delisted names** — survivorship bias inflates backtests. Store corporate actions (splits/dividends) for correct adjustment.

## Open questions

- Primary news provider for MVP (Alpaca WebSocket vs. Benzinga).
- Snapshot persistence target (object storage vs. QuestDB) across container restarts.
