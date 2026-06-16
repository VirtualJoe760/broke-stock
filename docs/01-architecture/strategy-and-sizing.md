# Strategy & sizing

## Responsibility

Convert scored signals into target positions. Mostly **deterministic math**, not LLM (the LLM scores; code sizes). Keeping this deterministic is what lets a strategy be backtested and climb the [validation ladder](../05-research/validation-methodology.md).

## Flow

1. **Aggregate** per-ticker signals over a decay window (recent > stale) → a per-ticker score.
2. **Filter** with structured factors: liquidity, volatility, existing position, regime gate (e.g. VIX threshold).
3. **Size** — map score → target weight via a defined rule (volatility-scaled / fractional Kelly, capped).
4. **Sanity pass (optional)** — Claude reviews the *portfolio* ("are these all the same macro bet?"), advisory only.

## Signal decay

Signals lose weight with age on a defined function (e.g. exponential half-life tuned per horizon). The half-life is a parameter validated by walk-forward ([self-improvement & optimization](self-improvement-and-optimization.md)), not hand-picked.

## Sizing rules

- Per-strategy sizing rule lives in a versioned **parameter file** (kept simple to avoid overfitting).
- Hard caps applied here *and* re-checked at the [risk gate](risk-gate.md) (defense in depth).

## Options sizing ([ADR-005](../00-overview/decisions-log.md))

LEAPS/options sizing is **premium-based and total-loss-aware** — size by premium-at-risk, not notional, because OTM options can go to zero. The wheel ([strategy 003](../04-strategies/003-the-wheel-options-income.md)) sizes by cash-secured collateral.

## Parameters are frozen for live

A live strategy runs **validation-cleared, frozen** parameters. Improvements re-enter via the ladder, never by hot-patching the live strategy ([ADR-009](../00-overview/decisions-log.md)).

## Open questions

- Default sizing rule (vol-scaling vs. fractional Kelly) for the first validated strategy.
- Decay half-lives per horizon (to be fit walk-forward).
