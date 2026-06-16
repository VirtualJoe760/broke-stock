# Self-improvement & optimization

> Status: drafted. Surfaced by [digest 003](../05-research/video-digests/003-hermes-self-improving-agent.md). This is the "holy grail" — and the easiest way to blow up.

## The appeal and the trap

A trading agent that learns from its mistakes and improves its own strategy is the dream. The trap: **an agent that optimizes against its own recent results will overfit, and can reward-hack the target metric — confidently tuning itself into a blow-up.** Self-improvement without an out-of-sample gate is a machine for manufacturing false confidence.

The hard part of a self-improving agent is **not** building the loop. It's **proving each improvement is real and not curve-fitting.** That is the entire job of this document.

## What makes a good trading agent (the 4-criteria rubric)

From digest 003, mapped to where we handle each:

| Criterion | Meaning | Where it lives here |
|---|---|---|
| **Accuracy** | precise, consistent, objective input data | [data & ingestion](data-and-ingestion.md), point-in-time storage |
| **Reliability** | 24/7, survives a machine going down | [agent runtime & scheduling](agent-runtime-and-scheduling.md) (cloud routines) |
| **Defined goal** | quantitative **success AND failure** (target Sharpe, max DD, kill thresholds) | [strategy template](../04-strategies/_TEMPLATE.md), [risk gate](risk-gate.md) |
| **Self-improvement** | learn → hypothesize → change one variable → re-test → new baseline | this doc + [validation methodology](../05-research/validation-methodology.md) |

## Self-improvement done right vs. wrong

**Right (walk-forward, out-of-sample):**
- Optimize parameters on an **in-sample** window only.
- Change **one variable at a time** (the scientific method) so you know what caused any change.
- **Freeze** the new parameters, then measure them on an **out-of-sample** window the agent never saw.
- Promote only if the change holds out-of-sample and across regimes. New baseline. Repeat (walk-forward).

**Wrong (what the video does implicitly):**
- Let the agent rewrite its strategy against its **own recent live results**, on **real money**, with no held-out test. This fits noise, chases the last regime, and reward-hacks the metric.

## The gated loop ([ADR-009](../00-overview/decisions-log.md))

```
propose change (one variable)
  → optimize on in-sample
  → FREEZE params
  → prove on out-of-sample holdout (+ across regimes)
  → if it holds: promote to new baseline → paper → live
  → if not: discard, log the lesson
```

- **Allowed:** the loop runs continuously in research/backtest and on paper.
- **Forbidden:** the loop modifying a strategy that is trading **live capital**. Live runs use *frozen, validation-cleared* parameters. Improvements re-enter through the [validation ladder](../05-research/validation-methodology.md), not by hot-patching the live agent.

## Reward-hacking / Goodhart cautions

- "When a measure becomes a target, it ceases to be a good measure." An agent told to maximize Sharpe will find ways to game Sharpe (e.g. selling volatility / hidden tail risk) that look great until they don't.
- Guard with: out-of-sample testing, multiple metrics (return, drawdown, tail risk together), regime splits, and a human review gate on any parameter change before live.

## Multi-agent separation of concerns (optional pattern)

Digest 003 splits roles: one agent for portfolio mechanics/valuation, another for parameter optimization, on a time offset. Useful for isolating responsibilities and avoiding a single agent both trading and grading its own homework. If adopted, the optimizer never writes directly to live params — it proposes into the gated loop above.

## Bottom line

Build the self-improvement loop — it's worth it — but wire it so it can only ever *propose*, and only *out-of-sample-proven* changes reach real money. The loop is the easy 20%; the validation gate around it is the 80% that keeps the account alive.
