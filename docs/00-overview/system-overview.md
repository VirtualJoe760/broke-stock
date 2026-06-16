# System overview

## What `broke` is

An AI-assisted equities research-and-execution platform. One event-driven engine runs a single loop:

```
ingest market data + news
  → Claude scores it into structured signals
  → deterministic strategy + sizing
  → hard risk gate
  → execution
  → log / feedback
```

The same engine runs identically in **backtest → paper → live**; only the clock, data source, and execution venue swap. On top sit three human surfaces — a **content digest**, a **trader cockpit**, and a **Jarvis voice layer**.

The stance: this is **signal generation + augmentation with deterministic risk controls and a validation gate**, not autonomous money-printing. The [validation methodology](../05-research/validation-methodology.md) decides what is allowed near real capital.

## Layers

1. **Data & ingestion** — real-time + historical feeds (Alpaca → Polygon → Databento as fidelity climbs) + news/filings/transcripts; point-in-time storage with ingest timestamps. ([detail](../01-architecture/data-and-ingestion.md))
2. **Signal / intelligence (Claude)** — text → typed signal (`event_type`, `sentiment`, `surprise`, `magnitude`, `confidence`, `horizon`); structured output, model tiering, prompt caching. ([detail](../01-architecture/signal-layer.md))
3. **Strategy & sizing** — deterministic: signal aggregation → target weights → vol-scaled sizing. ([detail](../01-architecture/strategy-and-sizing.md))
4. **Risk gate** — hard, code-enforced limits + kill switch; the human-approve/autopilot toggle. ([detail](../01-architecture/risk-gate.md))
5. **Execution** — broker adapters (Alpaca/IBKR) behind a stable interface; bracket/OCO orders. ([detail](../01-architecture/execution.md))
6. **Persistence & events** — Postgres/Neon + Drizzle; event log (Redis Streams → NATS/Redpanda); immutable tick/order/fill events. ([detail](../01-architecture/persistence-and-events.md))
7. **API / orchestration** — FastAPI (REST + WebSocket) bridging the Python engine to the web/voice layers. ([detail](../01-architecture/api-orchestration.md))
8. **Frontend** — Next.js + TS; [content dashboard](../02-frontend/content-dashboard.md) + [trader dashboard](../02-frontend/trader-dashboard.md); TradingView Lightweight Charts.
9. **Voice & alerts** — custom [Jarvis MCP](../03-voice-and-alerts/jarvis-mcp.md) (domain brain) + ElevenLabs (audio); scheduler + [alert engine](../03-voice-and-alerts/alerts-and-notifications.md).
10. **Compliance & audit** — PAPER/LIVE separation, audit trail, disclosures, recordkeeping. ([detail](../06-compliance/regulatory-and-risk.md))

## The load-bearing principle

**One engine, swappable clock + data source + execution venue.** Get this right and backtest→paper→live needs no rewrite; get it wrong and the proven edge evaporates against a live feed. See [engine & parity](../01-architecture/engine-and-parity.md) and [ADR-001](decisions-log.md).

## Runtime (how it actually runs)

Two philosophies, used as a hybrid ([agent runtime & scheduling](../01-architecture/agent-runtime-and-scheduling.md), [ADR-007](decisions-log.md)):
- **Deterministic engine** (NautilusTrader) for backtestable strategy logic — the part that must be *proven*.
- **Agentic runtime** (Claude Code Routines, scheduled cloud agents with file-based memory) for orchestration: research, monitoring, alerting, and proposing trades. Fast to ship a 24/7 paper agent — but the *edge* stays in deterministic, testable rules, never in an un-backtestable agent loop.

## Stack at a glance

| Layer | Choice |
|---|---|
| Trading engine | NautilusTrader (Rust core / Python API) |
| Engine / AI / voice-brain language | Python 3.12+ |
| AI signal | Anthropic SDK (Claude), structured output + caching |
| Market data | Alpaca → Polygon → Databento (L2/MBO) |
| Time-series | DuckDB + Parquet (research), QuestDB (live ticks) |
| App DB | Postgres on Neon + Drizzle ORM |
| Event bus | Redis Streams → NATS/Redpanda |
| API | FastAPI (REST + WebSocket) |
| Frontend | Next.js + React + TS, TradingView Lightweight Charts |
| Voice | Custom Jarvis MCP + ElevenLabs MCP/API |
| Alerts | Scheduler + event engine + Twilio / push / spoken |
| Auth | better-auth |

## Deployment & distribution

- **Cloud API default, no GPU required** — Claude via API behind a swappable provider interface; optional small-model triage on the Mac mini ([ADR-011](decisions-log.md), [model hosting](../08-deployment/model-hosting.md)).
- **Containerized, multi-arch, 12-factor** — develop on Windows, run on the Mac mini (ARM), deploy to a Linux VPS (x86) with no porting ([ADR-013](decisions-log.md), [deployment & portability](../08-deployment/deployment-and-portability.md)).
- **Self-hostable, single-tenant, clone & deploy** — each user runs their own instance with their own keys; we don't hold others' funds/credentials ([ADR-012](decisions-log.md), [distribution](../08-deployment/distribution.md)).

## Positioning (current)

**Augmentation, not alpha** ([ADR-014](decisions-log.md)). Preliminary edge tests found no tradeable signal in the easy data ([edge findings](../05-research/edge-findings.md)), so the product's value is research + monitoring + disciplined process + the validation engine — it does not promise market-beating returns. Trading capability (paper-first, swing/event-driven equities + LEAPS, human-in-the-loop, hard risk gate) remains a feature; any strategy must clear the [validation ladder](../05-research/validation-methodology.md) before live capital. Not intraday/day-trading ([ADR-002](decisions-log.md)).
