# Build log

Append-only record of autonomous build passes so progress is reviewable. Newest at top.

---

## Pass 18 — 2026-06-16 — Polygon/Massive price adapter (for the real L2)

Done:
- `broke_engine/data/polygon_store.py` — `PolygonPointInTimeStore` implementing `PointInTimeStore` over Polygon daily aggregates (point-in-time `ts <= as_of`). Configurable host (`POLYGON_BASE_URL`, default api.polygon.io) since Polygon rebranded to "Massive".
- `config.polygon_base_url` added. Not imported in `data/__init__` (keeps the suite httpx-free); import via `broke_engine.data.polygon_store`.
- Imports clean in the venv; 31 tests still pass. **UNVERIFIED against the live API** — needs a real `POLYGON_API_KEY` + network; host may need switching to api.massive.com.

Pending: user signs in to Massive (Polygon) and adds `POLYGON_API_KEY` → then run the real(er) L2 on real prices + real post-cutoff headlines.

---

## Pass 17 — 2026-06-16 — LIVE brain verified + L2 event-study pipeline

Done:
- **Live Claude call VERIFIED** (real key + credits): `score_news` returned a calibrated `Signal` (NVDA, macro, surprise 0.25, confidence 0.55 — correctly skeptical that the move was already priced in). The brain works end-to-end.
- `config.py` now loads `services/engine/.env` + repo-root `.env`/`.env.local` (cwd-independent).
- **L2 event-study harness** `broke_engine/research/event_study.py`: score each news event → join realized forward return from a PointInTimeStore → bucket by surprise/sentiment → long-short spread. `test_event_study.py` (FakeProvider, no Anthropic) green; **31 tests total**.
- `scripts/event_study_demo.py` ran live (3 Claude calls) end-to-end: n=3, spread computed. **Explicitly pipeline-only — synthetic prices, so the returns are meaningless.**

⚠️ For a REAL L2 verdict (does the signal actually predict returns?): needs REAL point-in-time news + prices (Alpaca/Polygon) and **post-training-cutoff dates** (else data leakage). That data wiring is the next unlock — needs Alpaca/Polygon keys.

---

## Pass 16 — 2026-06-16 — live brain wired (needs ANTHROPIC_API_KEY to run)

Done (code written; runs once a key is present):
- `AnthropicProvider.complete` implemented for real — calls the Anthropic SDK, forces **structured output** via a single `emit` tool whose input matches a JSON schema, caches the system block. Plain-text path too.
- `broke_engine/signals/scorer.py` — `score_news(provider, ticker, headline, context)` → validated `Signal` (calibrated system prompt; surprise = not-yet-priced-in).
- `scripts/score_demo.py` — one-command smoke test.
- **VERIFIED (offline):** modules import without the SDK/key; provider resolves to `claude-opus-4-8`; all 30 tests still pass. (A live call needs the key — not run here; that would spend your tokens.)

To run it: see "Wire the real brain" steps in the chat / below. Next after keys: Alpaca data adapter + the L2 event study.

---

## ✅ BUILD COMPLETE (key-free scope) — loop stopped (2026-06-16)

Everything buildable without real keys/data/trades is done, committed on `build/foundation`, and pushed to GitHub. **No keys used, nothing traded, nothing sent.** 15 commits.

### Built & verified
- **Engine (Python), 30 tests passing:** point-in-time data store (no-lookahead), Claude signal schema, strategy sizing (decay + vol-scaled), risk gate (limits + kill switch), execution adapter + simulated matcher, wheel backtest harness, alert engine (rules + NoopDispatcher).
- **API:** FastAPI endpoints + WebSocket stub (POST /orders proposes only) — py_compile verified.
- **Frontend (Next.js), `next build` passes:** landing + `/trader` cockpit (positions, AI proposal approve/reject, risk panel, kill switch, equity chart) + `/digest` (AI brief, theses, scored news, curated media), all on mock data.
- **CI:** GitHub Actions (engine ruff+pytest; web npm ci + next build).

### Needs you (real keys / data / supervision — by design)
1. **No edge proven.** Wheel metrics are mock/proxy noise (pre-L2). First real work: implement `AnthropicProvider.complete`, wire real market data into `DuckDBPointInTimeStore`, and run the **L2 event study**.
2. **Engine venv:** the machine's global FastAPI/starlette are mismatched — create a venv in `services/engine` and `pip install -e ".[dev]"` so the API runs and CI mirrors local.
3. **Heads-up for CI / clean clones:** `apps/web/package.json` currently has a `thinkbigjoe: file:../../../thinkbigjoe` dependency (points outside the repo). It works on this machine but will break `npm ci` in CI and on a fresh clone — recommend removing it.
4. Add real keys to a local `.env` (Anthropic, Alpaca **paper**) — never in chat. Ships in paper mode; nothing trades until you opt in.

### Review
`git checkout build/foundation` (or open the PR). Engine: `cd services/engine && pytest`. Web: `cd apps/web && npm run dev`.

---

## Pass 15 — 2026-06-16 — CI workflow + full suite green

Done:
- `.github/workflows/ci.yml` — engine job (setup-python, `pip install -e ".[dev]"`, ruff, pytest) + web job (setup-node, `npm ci`, `npm run build`).
- **VERIFIED:** full engine suite `30 passed` locally.

Key-free scope complete → **loop stopped** (no further wakeup).

---

## Pass 14 — 2026-06-16 — alert engine skeleton

Done:
- `broke_engine/alerts/` — `AlertRule`/`Alert`/`AlertType`/`Tier`, a pure `evaluate(rules, state)` (price target → notice, stop → urgent, daily-loss → critical, high-confidence signal → notice), and an `AlertDispatcher` interface with `NoopDispatcher` (records would-be sends, **NO real network send**).
- `test_alerts.py` (5 cases). **Verified offline:** all tiers fire correctly; signal matches only the high-confidence ticker; NoopDispatcher records 1 and sends nothing.

Last chunk next: (E) GitHub Actions CI (engine ruff+pytest, web next build) + final summary, then the loop stops.

---

## Pass 13 — 2026-06-16 — FastAPI endpoints + WebSocket stub

Done:
- `broke_engine/mockdata.py` — engine-side mock data (portfolio, positions, orders, strategies, signals, digest, alerts).
- Expanded `broke_engine/api.py` with REST endpoints from the API doc: GET /health, /portfolio, /positions, /orders, /strategies, /signals, /digest/today, /alerts; **POST /orders returns a *proposed* order only (never executes)**; plus a `/ws` WebSocket stub.
- **VERIFIED:** `py_compile` clean on api.py + mockdata.py; mockdata loads (3 positions, 3 strategies).

⚠️ ENV NOTE (for the user, not a code bug): the globally-installed FastAPI/starlette are version-mismatched (`Router.__init__() got an unexpected keyword 'on_startup'`), so a *runtime* import fails. Fix by using a venv with the pinned deps: `python -m venv .venv` in services/engine, then `pip install -e ".[dev]"`. The code itself is standard FastAPI and parses cleanly.

Next: (D) alert engine skeleton (rule eval + NoopDispatcher, with tests), then (E) CI workflow + more tests.

---

## Pass 12 — 2026-06-16 — content digest page

Done:
- `apps/web/app/digest/page.tsx` — content digest on mock data: AI daily brief hero + key points, "why we hold" position theses (surprise + P&L), scored news feed with priced-in flag, curated media cards.
- **VERIFIED:** `next build` exit 0; `/digest` in the route list (6 static pages). Both dashboards build cleanly.

Frontend (landing + /trader + /digest) is functionally complete on mock data. Next: FastAPI endpoints (B) returning mock/stub data + WebSocket stub, then alert/agent stubs (D), CI (E).

---

## Pass 11 — 2026-06-16 — trader cockpit page (+ deps installed, build verified)

Done:
- `apps/web/app/trader/page.tsx` — the trader cockpit on mock data: MODE banner, portfolio metric cards, **equity curve** (lightweight-charts, dynamically imported client-side), positions blotter with AI confidence, **AI proposal approve/reject** (stateful), order ticket, risk bars + **kill switch**.
- Ran `npm install` (Next 15 + react + lightweight-charts) and committed `package-lock.json`.
- **VERIFIED:** `next build` compiled successfully, types valid, static pages generated for `/` and `/trader` (exit 0). The page is real, not just plausible.

Next: `/digest` content page (AI brief, theses, scored news), then FastAPI endpoints, alert/agent stubs, CI.

---

## Pass 10 — 2026-06-16 — Next.js frontend scaffold

Done (hand-written, no npm install yet):
- `apps/web` — Next.js App Router + TS scaffold: `package.json` (next/react/lightweight-charts), `tsconfig.json`, `next.config.mjs`, root `layout.tsx`, dark-theme `globals.css`, landing `page.tsx` (PAPER banner + links to /trader and /digest).
- `lib/mock.ts` — shared paper-mode mock data (portfolio, positions w/ AI confidence, AI proposal, scored news, daily brief, equity curve, risk state) for the dashboards.

Not verified in-browser: needs `npm install` (a network op left for the user / a later pass) — node_modules absent, so no preview yet.

Next: `/trader` cockpit page, then `/digest` page (consuming lib/mock), then FastAPI endpoints, alert/agent stubs, CI.

---

## Pass 9 — 2026-06-16 — execution adapter + simulated matcher

Done:
- `broke_engine/execution/` — `ExecutionAdapter` interface + `Order`/`Fill` + `SimulatedMatcher` (paper fills: slippage by side, commission, **idempotent** client_order_id so resubmits never double-fill, net position tracking).
- `test_execution.py` (5 cases). **Verified offline:** buy 100→100.1, sell 100→99.9, idempotent (pos 5 not 10), commission 1.0, net position 6.

The deterministic Python core is now complete and tested: **data store, signal schema, sizing, risk gate, execution, wheel harness.**

Next: the **Next.js frontend** in apps/web (trader cockpit + content digest on mock data) — needs an `npm` install (network); if unavailable, commit the hand-written app source and note it. Then FastAPI endpoints, alert/agent stubs, CI.

---

## Pass 8 — 2026-06-16 — strategy & sizing

Done:
- `broke_engine/strategies/sizing.py` — `decayed_score` (time-decay + confidence-weighted signal aggregation, surprise-weighted), `daily_volatility_pct`, `target_weight` (vol-scaled, capped, min-conviction gate), `SizingParams`.
- `test_sizing.py` (7 cases). **Verified offline:** empty→0, recent outweighs stale, cap at 5%, below-min→0, lower vol→larger size, vol calc correct.
- Bugfix caught by verification: `Signal.rationale` now defaults to "" (it isn't a required schema field) so signals construct without it.

Next: execution adapter interface + simulated matcher (paper fills), then the Next.js frontend.

---

## Pass 7 — 2026-06-16 — risk gate (build resumed, broader scope)

Build **resumed** with an expanded scope: now building everything that needs no real keys/data/trade — frontend, API endpoints, deterministic logic, alerts, tests.

Done:
- `broke_engine/risk.py` — `RiskGate` + `RiskLimits` (max position %, gross exposure %, daily-loss kill switch, weekly new-position cap, options ban), `OrderIntent`, `AccountState`, `RiskDecision`.
- `test_risk.py` (6 cases). **Verified offline:** clean order approved; oversized / options / weekly-cap rejected; daily-loss trips kill switch; options allowed when enabled.

Next: strategy & sizing (signal aggregation + vol-scaled sizing), execution adapter + simulated matcher, then the Next.js frontend (needs an npm install), API endpoints, alert/agent stubs, CI.

---

## (superseded) Phase 0 + Phase 1 skeleton complete — build later RESUMED with broader scope (2026-06-16)

Phase 0 + the Phase 1 skeleton are done. The loop has ended itself per its stop condition. Everything is committed on `build/foundation` and pushed to GitHub. **No keys were used, nothing traded, nothing spent.**

### What's built (and verified to run offline)
- **Phase 0:** monorepo + docker-compose + `.env.example`; engine config + **swappable LLM provider** (Anthropic default / OpenAI-compatible for triage); FastAPI skeleton (`/health`, `/portfolio` stubs) + Dockerfile; **Drizzle schema** (accounts, strategies w/ L0–L5, orders, positions, fills, audit).
- **Phase 1 skeleton:** **point-in-time data store** (no-lookahead, verified); **signal schema** (validated, JSON-schema for structured output, verified); **wheel backtest harness** (runs over mock data, emits return/drawdown/premium/assignment metrics, verified).

### Honest status — what is NOT done (needs you + supervision)
- **No real edge demonstrated.** The wheel "result" is synthetic-data + proxy-premium noise — pre-L2. Nothing has climbed the validation ladder.
- **Stubs awaiting keys/data:** `AnthropicProvider.complete` (needs `ANTHROPIC_API_KEY`), `DuckDBPointInTimeStore` (needs real market data via Polygon/Alpaca), the wheel's proxy premiums (need a real option chain/IV).
- **Deferred Phase 0 niceties** (need npm/network): Next.js web scaffold, CI multi-arch image build.

### Your move in the morning (supervised)
1. `git -C F:\web-clients\joseph-sardella\broke push` is already working — review `build/foundation` (or open the PR) and merge when happy.
2. Put real keys in a local `.env` (Anthropic, Alpaca **paper**) — never in chat.
3. Then the first real work: implement `AnthropicProvider.complete`, wire a real data source into the point-in-time store, and run the **L2 event study** to find out if any signal/strategy actually predicts returns. That's the first real test of edge.

### Run it yourself
```
$env:PYTHONPATH="F:\web-clients\joseph-sardella\broke\services\engine"
python -c "from datetime import datetime,timezone; from broke_engine.data.store import MockPointInTimeStore; from broke_engine.strategies import WheelBacktest; print(WheelBacktest(MockPointInTimeStore()).run('WHEEL', datetime(2024,1,1,tzinfo=timezone.utc), datetime(2024,12,31,tzinfo=timezone.utc)))"
```

---

## Pass 6 — 2026-06-16 — Phase 1: wheel backtest harness

Done:
- `broke_engine/strategies/wheel.py` — `WheelBacktest` over `PointInTimeStore`: cash-secured puts → assignment → covered calls, with metrics (return, max drawdown, premium collected, assignment loss, cycles).
- Test `test_wheel.py`; **verified offline:** 13 cycles, +2.15%, 0% DD on mock data (0 assignments — artifact of upward-drift synthetic series + proxy premiums; explicitly pre-L2, not real edge).
- Premiums are crude proxies (no real IV/Greeks) — clearly caveated in code; replaced by real option data before any result is trusted.

Phase 1 skeleton complete → **loop stopped**.

---

## Pass 5 — 2026-06-16 — Phase 1: signal schema

Done:
- `broke_engine/signals/` — the `Signal` schema (stdlib dataclass + enums: `EventType`, `Magnitude`, `TimeHorizon`) with range validation (sentiment -1..1, surprise/confidence 0..1).
- `Signal.from_dict()` to parse LLM JSON (string enums coerced); `signal_json_schema()` for the structured-output tool the LLM must call.
- Test `test_signal.py` (valid parse, out-of-range rejected, schema required fields).
- **Verified offline:** parses a sample signal, rejects sentiment=1.5, schema required fields correct.

Next (last Phase 1 chunk): the wheel backtest/event-study harness over MockPointInTimeStore — produces metrics with no keys.

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
