# Digest 002 — 24/7 trading agent with Claude Code Routines

- **Source:** YouTube — building a 24/7 AI trading agent with Claude Code Routines (creator previously ran an "OpenClaw" agent challenge vs. a friend).
- **Prior result claimed:** OpenClaw agent, $10,000, 30 days, **beat the S&P by ~8%**, on Opus 4.6.
- **This video:** migrate that agent off OpenClaw to **Claude Code Routines** (cloud cron) on Opus 4.7, running 24/7.
- **Extracted strategy:** [002 — fundamentals, beat the benchmark](../../04-strategies/002-fundamentals-beat-spx.md)

## What he actually built

A scheduled, file-memory agent — no custom engine, no OpenClaw/agent-SDK:

- **Scheduler:** Claude Code Routines (remote/cloud cron, GitHub-backed).
- **Model:** Opus 4.7.
- **Broker:** Alpaca API ($100k paper account; real money needs verification).
- **Research:** Perplexity API (chosen over built-in web search).
- **Notifications:** ClickUp (could be Slack/Telegram/WhatsApp).
- **Memory:** file-based — agent wakes stateless, reads files, acts, writes lessons, commits to GitHub so the next run sees them.

**Schedule:** weekdays 6:00 (pre-market research/ideas), 8:30 (execute trades, 10% trailing stop), 12:00 (cut losers −7%, tighten winners), 15:00 (review), Fri 16:00 (weekly review → ClickUp with portfolio, return vs. SPX, trade history, self-grade — graded itself "C").

**Safeguards:** start paper; ≤5% per position; daily loss limit; max 3 new positions/week; **no options**; explicit allowed/forbidden actions; human reviews each run's transcript.

**Migration craft:** exported 7 context files from the old agent (instructions, strategy, trade/research logs, weekly reviews), had Claude restructure them for Routines, then committed. Caught a **leaked Alpaca API key** in the old template — moved all secrets to environment variables.

## Strategy stance

Explicitly **fundamentals-based, long-term / swing — not day trading.** Goal is simply to beat the S&P. Notes that Opus 4.7 scored *lower than 4.6* on an "agentic financial analysis" benchmark, argues that benchmark measures fundamental-analysis quality (not day-trading/technical timing) and so still suits his approach.

## Honest read

- **One month, one account, single regime, unlevered equities.** "Beat S&P by ~8% in a month" with no Sharpe/drawdown/sample is an anecdote — and 8% over the index in a month usually means higher beta/concentration in an up tape. Enters our system at **L0**. (More sober than digest 001: no options leverage.)
- **The methodology is genuinely disciplined** and aligns with us: paper-first, explicit safeguards, no options for the autonomous agent, human review of every run, weekly self-grading.
- **The benchmark caveat cuts both ways.** If the agentic-*financial-analysis* benchmark dropped 4.6→4.7 and the strategy *is* fundamentals, that's a yellow flag for that upgrade on this task. Lesson for us: choose the model by our own validated results, not headline scores.
- **Biggest contribution = the runtime pattern**, not the returns: Claude Code Routines as a 24/7 agentic runtime + file-based memory. See [agent runtime & scheduling](../../01-architecture/agent-runtime-and-scheduling.md).

## What we adopt vs. reject

**Adopt:**
- **Claude Code Routines** as a candidate orchestration runtime ([ADR-007](../../00-overview/decisions-log.md)).
- **File-based memory architecture** (read → act → write → commit) ([ADR-008](../../00-overview/decisions-log.md)).
- **Env-var secrets, never committed** (the leaked-key lesson) — [compliance](../../06-compliance/regulatory-and-risk.md).
- The **reference schedule** and the **safeguards list** (→ [risk gate](../../01-architecture/risk-gate.md)).
- **Perplexity** as a research source ([data & ingestion](../../01-architecture/data-and-ingestion.md)); **ClickUp/Telegram** as alert channels ([alerts](../../03-voice-and-alerts/alerts-and-notifications.md)).

**Reject / gate:**
- The result as evidence — L0 hypothesis only.
- **Agentic-only with no backtestable core.** A file-reading agent loop can't be validated rigorously; we keep deterministic, testable strategy logic and the [validation ladder](../../05-research/validation-methodology.md). Routines change how we run, not whether we prove.
