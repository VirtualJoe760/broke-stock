# Roadmap / phasing

The build order is driven by the [validation methodology](../05-research/validation-methodology.md): prove edge cheaply before building expensive realism.

## Phase 0 — Research & docs (current)

- Strategy library + validation ladder established.
- Digest videos/ideas → L0 hypotheses → L1 logic checks.
- No code, no capital. Goal: a shortlist of strategies worth the engineering cost.

## Phase 1 — Proof of edge (MVP)

- **Signal-validation harness (L2):** event studies on the surviving L1 strategies — does the signal predict forward returns after costs?
- Minimal engine: NautilusTrader + DuckDB/Parquet + Alpaca free data.
- FastAPI + a thin Next.js dashboard (mock → real data), paper only.
- Goal: at least one strategy reaches **L3 backtest** with metrics meeting thresholds.

## Phase 2 — Realism & the product surfaces

- Data tier up: Polygon real-time, QuestDB tick capture, Databento L2 where needed.
- Options/Greeks module ([ADR-005](../00-overview/decisions-log.md)); 4-layer daily-monitoring design.
- Content dashboard + trader cockpit built for real.
- Jarvis MCP + ElevenLabs briefings; scheduler + Telegram/SMS alerts.
- Latency/slippage/spread modeling. Goal: strategies reach **L4 paper-proven**.

## Phase 3 — Live (graduated) & scale

- Live broker adapter behind the same interface; **L5** with capped real size.
- Event-sourced bus (NATS/Redpanda), multi-strategy portfolio, full audit/compliance.
- Conversational Jarvis. Autopilot only per [ADR-004](../00-overview/decisions-log.md).

## Standing cadence (every new video/idea)

Digest → L0 → L1 logic check → L2 event study → (only if it survives) L3+. Most ideas die in the first three steps, on paper, for free. That funnel is the point.
