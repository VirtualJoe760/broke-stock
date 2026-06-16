# Agent runtime & scheduling

> Status: drafted. Captures a real architectural fork surfaced by [digest 002](../05-research/video-digests/002-claude-routines-24-7-agent.md).

## Two runtime philosophies

There are two fundamentally different ways to run this system. They are not mutually exclusive — the recommendation is a hybrid.

### A — Deterministic engine (NautilusTrader)

A long-running Python service consumes an event stream and runs strategy code identically in backtest/paper/live ([engine & parity](engine-and-parity.md), [ADR-001](../00-overview/decisions-log.md)).

- **Strength:** true backtest parity → strategies can climb the [validation ladder](../05-research/validation-methodology.md) to "proven."
- **Cost:** more engineering; the strategy must be expressed as deterministic logic.

### B — Agentic runtime (Claude Code Routines)

Scheduled cloud agents ("routines") wake on a cron, read memory files, research, decide, trade via the Alpaca API, write lessons back, and commit to a GitHub repo. No custom engine.

- **Strength:** very fast to ship a live, paper, 24/7 agent; full agentic flexibility in volatile conditions; cheap to operate (≈$1–few per run vs. always-on API automation).
- **Cost / danger:** **an agentic file-reading loop cannot be cleanly backtested.** Each run is non-deterministic and path-dependent. This is in direct tension with "proven, tested results."

## The hybrid stance ([ADR-007](../00-overview/decisions-log.md))

- Use an **agentic runtime (Routines)** for *orchestration*: scheduled research, monitoring, alerting, and **proposing** trades (human-in-the-loop, paper).
- Keep the **strategy decision logic deterministic** wherever an edge is being claimed, so it remains backtestable and can be validated. The agent *executes and supervises*; the *edge* lives in testable rules.
- Never let the agentic runtime become an excuse to skip the validation ladder. Routines change *how* we run, not *whether* we prove.

## Hermes (Nous Research) — alternative agentic runtime

A recurring alternative in the reviewed videos ([digest 003](../05-research/video-digests/003-hermes-self-improving-agent.md), [digest 004](../05-research/video-digests/004-hermes-telegram-analyst.md)) is **Hermes**, an open-source agent framework by Nous Research: persistent memory, a built-in scheduler, a self-learning "skills" loop, and tools (web, code execution, computer use). It's used two ways — autonomously deployed on a VPS, or as a conversational analyst over Telegram/Discord (human-in-the-loop).

Stance: Hermes is a useful **reference** and we borrow its patterns (file memory, skills, messaging interface), but we do not hand our money-path to a black-box framework ([ADR-006](../00-overview/decisions-log.md), [ADR-007](../00-overview/decisions-log.md)). If used at all, it sits behind the same risk gate and validation ladder, with strict secrets/sandboxing (it can execute code and hold broker credentials).

## Claude Code Routines — operational notes

- **Local vs. remote:** local routines run only while the desktop app is open; **remote** routines run in the cloud 24/7 but require a **GitHub repo** (the cloud clones it per run).
- **Persistence:** each remote run is ephemeral — it must **commit and push** memory/log changes to `main` (enable branch pushes) or the next run won't see them.
- **Secrets:** API keys go in the cloud environment's **environment variables**, never in the repo or `CLAUDE.md` ([ADR-008](../00-overview/decisions-log.md), [compliance](../06-compliance/regulatory-and-risk.md)).
- **Context budget:** ~200k tokens per run. Treat tokens like money — keep memory files lean and load only what the run needs.
- **Model:** use the latest Opus. Note: pick the model by *our own validated results on our task*, not headline benchmarks — see [digest 002](../05-research/video-digests/002-claude-routines-24-7-agent.md) for the agentic-financial-analysis benchmark caveat.

## File-based memory architecture ([ADR-008](../00-overview/decisions-log.md))

A stateless run becomes a learning system through files:

```
wake → read memory files (state, strategy, logs)
     → act (research, decide, trade)
     → write lessons + update logs
     → commit + push
```

- `CLAUDE.md` — agent identity, rules, guardrails, how to use each file.
- `strategy.md` — the strategy spec (also the validated strategy from the library).
- `portfolio.md` / `positions.json` — current state.
- `trade-log.md`, `research-log.md` — history.
- `weekly-review.md` — self-graded performance report (→ ClickUp/Telegram).

## Reference schedule (weekdays, market open only)

| Time | Routine |
|---|---|
| 6:00 | Pre-market research → trade ideas (no action) |
| 8:30 | Execute planned trades; set trailing stops |
| 12:00 | Midday risk: cut losers, tighten winners' stops |
| 15:00 | Pre-close review |
| Fri 16:00 | Weekly review report (return vs. benchmark, trades, self-grade) |

## Safeguards (mandatory before any autonomy)

Position cap (e.g. ≤5% per position), daily loss limit, max new positions/week, instrument bans (e.g. no options for the autonomous agent), explicit allowed/forbidden actions. These map onto the deterministic [risk gate](risk-gate.md).
