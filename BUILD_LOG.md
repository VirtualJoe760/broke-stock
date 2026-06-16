# Build log

Append-only record of autonomous build passes so progress is reviewable. Newest at top.

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
