# Decisions log (ADRs)

Architecture Decision Records. Each captures a decision, why, and what would change it. Append-only; supersede rather than delete.

---

## ADR-001 — One engine, backtest/paper/live parity (NautilusTrader)

**Decision:** Build on a single event-driven engine where the same strategy code runs in backtest, paper, and live; only the clock, data source, and execution venue swap. Default engine: NautilusTrader.

**Why:** "Emulate direct access" and "prove an edge before going live" both require that the backtested code path *is* the live code path. NautilusTrader is purpose-built for this parity.

**Changes it if:** we find the learning curve / fit unworkable → fall back to a custom event-loop engine, preserving the same swappable-clock abstraction.

---

## ADR-002 — Default horizon is swing / event-driven, not day trading

**Decision:** The platform targets swing/position trading (days–weeks) and event-driven catalysts, plus long-dated options. Intraday/day-trading is explicitly out of scope for v1 (a possible later specialization: news-catalyst intraday momentum).

**Why:** The documented LLM edge (news/earnings sentiment, surprise, post-event drift) lives at the daily-to-multi-day horizon. LLM latency loses the speed race against HFT. Every real example reviewed (incl. [digest 001](../05-research/video-digests/001-brandon-claude-robinhood.md)) confirms swing/LEAPS, not scalping. Scalping attempts "died by spread costs."

**Changes it if:** an L4-validated intraday strategy emerges with edge after costs.

---

## ADR-003 — Validation before capital

**Decision:** No strategy touches real money before clearing the [validation ladder](../05-research/validation-methodology.md) to L4 (paper-proven). Strategies from videos/ideas enter at L0 as hypotheses.

**Why:** Single-month, leveraged, survivorship-biased anecdotes are the norm in this space. The validation engine is the actual product; it kills bad strategies cheaply.

**Changes it if:** never, in spirit. Thresholds within the ladder may be tuned.

---

## ADR-004 — Human-in-the-loop before autopilot

**Decision:** v1 is propose-and-approve (Claude proposes, human approves, code executes). Full autopilot is a later destination, gated on paper-proven results and a hardened risk gate.

**Why:** LLMs hallucinate and fail in downturns; the reviewed experiments that "worked" were human-in-the-loop. Autopilot multiplies the cost of every failure mode.

**Changes it if:** a strategy is L4/L5-proven *and* the risk gate has a track record of containing the failure cases.

---

## ADR-005 — Options (LEAPS) are a first-class strategy class

**Decision:** Support long-dated options (LEAPS) alongside cash equities, with a dedicated Greeks-monitoring module. Avoid illiquid small-cap options.

**Why:** Defined-risk, leveraged directional bets suit a swing/event thesis; the strongest reviewed result used exactly this. But leverage is not edge — it amplifies both outcomes, so the risk gate matters *more* here.

**Changes it if:** options modeling/validation proves intractable for our backtest fidelity.

---

## ADR-006 — Stack baseline

**Decision:** Python engine (NautilusTrader) + FastAPI; DuckDB/Parquet + QuestDB for time-series; Postgres/Neon + Drizzle for app state; Next.js frontend; custom Jarvis MCP + ElevenLabs for voice; scheduler + Twilio for alerts.

**Why:** Matches the quant/ML ecosystem (Python), the team's web competency (Next.js/Drizzle/Neon), and the parity requirement. The engine is a stateful long-running service — it does **not** run on serverless/Vercel; only the frontend does.

**Changes it if:** scale or data-fidelity needs push specific components (e.g. Redpanda over Redis Streams) — already anticipated in phasing.

---

## ADR-007 — Hybrid runtime: agentic Routines for orchestration, deterministic logic for edge

**Decision:** Use an agentic runtime (Claude Code Routines — scheduled cloud agents) for *orchestration* (research, monitoring, alerting, proposing trades, human-in-the-loop on paper). Keep the *strategy decision logic* deterministic wherever an edge is claimed, so it stays backtestable. The agent executes and supervises; the edge lives in testable rules.

**Why:** Routines ship a 24/7 paper agent fast and handle volatile conditions flexibly. But an agentic file-reading loop **cannot be cleanly backtested** — directly opposed to "proven, tested results." The hybrid keeps speed without abandoning the [validation ladder](../05-research/validation-methodology.md). Surfaced by [digest 002](../05-research/video-digests/002-claude-routines-24-7-agent.md). Detail: [agent runtime & scheduling](../01-architecture/agent-runtime-and-scheduling.md).

**Changes it if:** Routines prove too limited (then a custom scheduler drives the same deterministic logic), or a rigorous way to validate fully-agentic loops emerges.

---

## ADR-008 — File-based memory architecture for stateless agent runs

**Decision:** Each scheduled run is stateless and learns through files: read memory (state, strategy, logs) → act → write lessons → **commit & push** to the repo so the next run sees them. `CLAUDE.md` holds identity/rules/guardrails; separate files hold state, trade/research logs, and the weekly review. Secrets live in **environment variables**, never in the repo or `CLAUDE.md`.

**Why:** Remote routines are ephemeral; persistence requires committing memory back to GitHub. Lean memory files respect the ~200k-token per-run budget. A reviewed source leaked an Alpaca key by committing it — secrets-in-env is the fix. Surfaced by [digest 002](../05-research/video-digests/002-claude-routines-24-7-agent.md).

**Changes it if:** we move to a stateful long-running service (Approach A), where memory is a database rather than committed files.

---

## ADR-009 — Self-improvement runs inside the validation framework

**Decision:** A strategy may have a self-improvement / optimization loop, but it runs **inside** the validation framework: optimize on in-sample, change one variable at a time, freeze parameters, prove on an out-of-sample holdout (and across regimes), then promote. The loop may run continuously in research/paper. It **may not** modify a strategy trading live capital — live uses frozen, validation-cleared parameters; improvements re-enter via the ladder, not by hot-patching the live agent.

**Why:** A self-improving agent that optimizes against its own recent results overfits and reward-hacks the target metric (Goodhart) — confidently tuning into a blow-up. Out-of-sample testing is the only thing that distinguishes real improvement from curve-fitting noise. Surfaced by [digest 003](../05-research/video-digests/003-hermes-self-improving-agent.md). Detail: [self-improvement & optimization](../01-architecture/self-improvement-and-optimization.md).

**Changes it if:** never in spirit. The mechanics (window sizes, promotion thresholds) may be tuned.

---

## ADR-010 — Asset scope: equities + options for v1; crypto out of scope

**Decision:** v1 trades US cash equities and long-dated options (LEAPS). Crypto is out of scope.

**Why:** Our edge research, data tiers, validation methodology, and regulatory framing are all built around equities. Crypto has different microstructure, 24/7 sessions, distinct regulation, and is where the riskiest reviewed examples concentrated (digest 003: real-money 30-min crypto). Staying focused keeps the validation work coherent.

**Changes it if:** an equities track is L4-proven and there's a deliberate, separately-validated case for adding a crypto track.

---

## ADR-011 — Cloud API default, swappable LLM provider, no GPU required

**Decision:** LLM calls go through one provider interface. Default = Claude via the Anthropic API. No GPU is required to run the system. Local/self-hosted models are optional and added later behind the same interface; the one early local use is small-model **triage** on the Mac mini (via Ollama) for high-volume news classification, with Claude doing the analysis.

**Why:** At our bursty/low-volume profile, API is cheaper than a 24/7 GPU. The open models good at the trading task are too big to self-host cheaply; the small ones we could host are weaker. Frontier API models are best at the reasoning that drives edge. Detail: [model hosting](../08-deployment/model-hosting.md).

**Changes it if:** sustained token volume gets high enough that a hosted model beats API on cost, or a privacy/offline requirement (e.g. from distribution) forces local inference.

---

## ADR-012 — Distribution: self-hostable, single-tenant, clone & deploy

**Decision:** Distribute as software each user deploys themselves — their own isolated instance, their own broker keys, on their machine or VPS. We do not host a multi-tenant app or hold others' credentials/money. Ships in paper mode with conservative defaults; nothing trades live until the user opts in.

**Why:** Hosting others' accounts/keys/funds means custody and heavy FINRA/SEC obligations. Single-tenant self-hosting sidesteps that and matches "clone & deploy from a VPS." Detail: [distribution](../08-deployment/distribution.md).

**Changes it if:** an equities track is L4-proven and there's a deliberate, separately-reviewed case for a hosted offering.

---

## ADR-013 — Containerized, multi-arch, 12-factor portability

**Decision:** Package the engine/agent/API as Docker images orchestrated by docker-compose; build **multi-arch** (`linux/amd64` + `linux/arm64`); follow 12-factor (config/secrets via env, no hardcoded OS paths, external state, reproducible builds). Develop on Windows, run on the Mac mini (ARM), deploy to a Linux VPS (x86) with no porting.

**Why:** The container is the portability layer — "moving the project" becomes clone + `compose up`. Multi-arch is required because the Mac mini is ARM and most VPS are x86, and some quant libs have native components. Detail: [deployment & portability](../08-deployment/deployment-and-portability.md).

**Changes it if:** never in spirit; specific orchestration (compose → k8s) may change at scale.
