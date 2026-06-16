# Build log

Append-only record of autonomous build passes so progress is reviewable. Newest at top.

---

## Pass 4 — 2026-06-16 — Phase 1: point-in-time data store

Done:
- `broke_engine/data/` — `Bar` model + `PointInTimeStore` interface.
- `MockPointInTimeStore`: deterministic seeded synthetic daily bars (weekdays), each bar's `ingest_ts == close time` so `as_of` enforces no-lookahead. Runs with zero keys/data.
- `DuckDBPointInTimeStore`: stub for the real Parquet/DuckDB store (filters `ingest_ts <= as_of`).
- Test `test_data_store.py` (no-lookahead + determinism).
- **Verified live** (stdlib only): 10 bars to the as_of date, no bar from the future, reproducible. This is the anti-data-leakage foundation the validation ladder depends on.

Next: Claude signal schema as pydantic models, then the wheel backtest/event-study harness on this mock data.

---

## Pass 3 — 2026-06-16 — Drizzle schema (app state)

Done:
- `packages/db`: Drizzle schema (`src/schema.ts`) for Postgres/Neon — `accounts`, `strategies` (with L0–L5 validation_level + frozen params), `orders` (idempotent client_order_id, correlation_id), `positions`, `fills`, `audit`.
- `package.json`, `drizzle.config.ts`, `tsconfig.json`, README.
- Migrations are generated against a real `DATABASE_URL` later — not during the offline build.

Phase 0 is essentially complete (engine config + LLM provider, FastAPI skeleton, Dockerfile, tests, DB schema). Remaining Phase 0 niceties deferred (need network/npm): Next.js web scaffold, CI multi-arch build.

Next: **Phase 1 skeletons** — DuckDB point-in-time data store interface (mock data), Claude signal schema as pydantic models, and the wheel backtest/event-study harness on synthetic data.

---

## Pass 2 — 2026-06-16 — engine API skeleton

Done:
- FastAPI app (`api.py`) with `/health` and `/portfolio` (stub, reflects paper mode).
- Entrypoint `__main__.py` (`python -m broke_engine`).
- Engine `Dockerfile` (multi-arch friendly).
- First test (`tests/test_llm_provider.py`) + mypy/pytest config.

Mode: paper/mock; no keys; endpoints return stubs. Next: Drizzle schema, then Phase 1 (DuckDB point-in-time store + signal schema + wheel backtest harness on mock data).

---

## Pass 1 — 2026-06-16 — Phase 0 kickoff

**Branch:** `build/foundation` (main holds the committed docs).

Done:
- Committed all documentation to `main` (root commit).
- Monorepo skeleton: `services/engine` (Python), `apps/web` (Next.js, placeholder), `packages/db` (Drizzle, placeholder).
- `docker-compose.yml` (api + redis + questdb; Postgres is external/Neon).
- `.env.example` with every config slot (no secrets).
- Engine foundation: `pyproject.toml`, `config.py` (env-driven), and the **swappable LLM provider interface** (`llm/provider.py`) with a Claude implementation stub + factory.

Mode: **paper / mock only**. No API keys present. No network calls that spend money. Nothing trades.

Blocked-on-human (for the morning):
- `gh auth login` so checkpoints can push to GitHub.
- Real API keys go in a local `.env` you control (Anthropic, Alpaca paper) — not in chat.

Next passes (planned):
- Finish Phase 0: engine entrypoint, FastAPI skeleton, Drizzle schema, Dockerfiles, CI for multi-arch.
- Begin Phase 1: point-in-time data store, signal schema, and the wheel's backtest/event-study harness against mock/sample data.
