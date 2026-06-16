# Risk gate

This is the layer that keeps the account alive. Every proposed order passes through it before execution. In autopilot it is the only thing between a hallucination and a loss; in human-in-the-loop it backstops the human.

## Hard, code-enforced controls (never LLM)

- Max position size; max gross/net exposure; sector/name concentration caps.
- Per-trade and **daily max-loss kill switch** (halts the loop; flatten or freeze).
- Liquidity check (exitable within N minutes of ADV).
- Sanity bounds — reject oversized orders; reject if price moved > X% since the signal.
- Volatility circuit breaker (e.g. VIX spike → de-risk/halt).
- Trade-count caps (e.g. ≤ N new positions/week) — from the reviewed safeguards.
- **Options-specific:** premium-at-risk caps; total-loss-aware sizing ([ADR-005](../00-overview/decisions-log.md)); ban naked options for the autonomous agent.

## Limit config (per deployment / strategy)

Limits live in config (env / per-strategy file), so self-hosters ship with conservative defaults and can tighten ([distribution](../08-deployment/distribution.md)). Example:

```
max_position_pct: 5
max_gross_exposure_pct: 60
daily_loss_limit_pct: 3
max_new_positions_per_week: 3
allow_options: false        # autonomous agent
```

## Human-in-the-loop toggle ([ADR-004](../00-overview/decisions-log.md))

This layer hosts the propose-and-approve gate. Live trades require explicit human approval until a strategy is paper-proven and the gate has a track record. Voice/chat can *propose*, never *fire* ([jarvis-mcp](../03-voice-and-alerts/jarvis-mcp.md)).

## Kill switch & breach handling

- Breach of a hard limit → block the order, log it, alert (urgent tier).
- Breach of the daily-loss limit → trip the kill switch: stop new orders, optionally flatten, notify.
- A strategy whose live results breach its validated envelope → **demote** it ([validation methodology](../05-research/validation-methodology.md)).

## Why it matters

Every reviewed blowup happened with **no guardrails** (e.g. a concentrated earnings bet, a self-modifying agent on real money). With leverage/options the gate matters *more*, not less.

## Open questions

- Flatten vs. freeze policy on kill-switch trip (per asset class).
- Where limit config is surfaced in the UI for self-hosters.
