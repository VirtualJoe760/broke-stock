# 003 — The wheel (options income)

- **ID:** 003
- **Status (validation level):** L0 — Hypothesis
- **Source:** [Digest 004 — Hermes Telegram analyst](../05-research/video-digests/004-hermes-telegram-analyst.md) (creator runs the wheel on options)
- **Instruments:** Options — cash-secured puts + covered calls on quality equities/ETFs
- **Time horizon:** Swing (option cycles, ~weekly to monthly)
- **Owner:** Joey
- **Last updated:** 2026-06-15

## Thesis (one sentence)

Systematically selling option premium on underlyings you'd be happy to own — cash-secured puts until assigned, then covered calls until called away — harvests volatility-risk premium as income, especially in flat-to-up, low-volatility regimes.

## Market regime assumptions

- **Needs:** flat-to-moderately-rising, lower-vol markets (the creator enters when VIX < 20).
- **Breaks / risk:** sharp drawdowns — cash-secured puts get assigned as the underlying gaps down, and covered calls cap the upside on the recovery. The classic failure mode is "pennies in front of a steamroller": steady income, occasional large drawdown. Income is *not* free money — it's compensation for tail risk.

## Rules (draft — make precise before L2)

- **Universe:** liquid, quality names / ETFs you are genuinely willing to own.
- **Entry (CSP):** sell a cash-secured put, ~30-delta, ~30–45 DTE, when regime filter passes (e.g. VIX < 20).
- **If assigned:** hold the shares, sell covered calls (~30-delta) until called away.
- **Management:** take profit at ~50% of max premium; roll or close at a defined loss / DTE threshold.
- **Position sizing / risk:** cash-secured (no naked exposure); per-name and sector caps; total-loss-aware on the underlying.

## Claimed results (from source) + credibility read

| Claimed | Reality check |
|---|---|
| (none — tutorial video) | No performance claim to assess. Credibility risk is the opposite: an affiliate-driven setup video, not evidence of edge. |

## Why this one is promising for validation

Unlike the discretionary strategies (001/002), the wheel is **rule-based and well-documented**, so it is **directly backtestable** — it can climb to L2/L3 faster and more cleanly. Good early candidate for the validation harness. The honest question a backtest must answer: does the premium collected actually exceed the drawdown cost across an up year *and* a down/choppy year, after commissions and assignment slippage?

## Validation log

| Level | Date | Result | Notes |
|---|---|---|---|
| L0 | 2026-06-15 | captured | from digest 004 |
| L1 | | pending | logic check |

## L1 logic-check questions

- Quantify the tail: model the wheel through a real drawdown (e.g. a −20% month) — what's the assignment loss vs. premium collected?
- Is the income edge real after commissions + assignment slippage, or just compensation for hidden short-vol risk?
- Does the VIX < 20 entry filter actually improve risk-adjusted returns, or just reduce activity?

## Open questions

- Which delta / DTE / profit-target combination is robust out-of-sample (not curve-fit)? See [self-improvement & optimization](../01-architecture/self-improvement-and-optimization.md).
- Single-name wheel vs. index-ETF wheel — which has the better risk-adjusted profile?

## Related strategies

[[001-leaps-catalyst-swing]] · [[002-fundamentals-beat-spx]] — all swing/options-or-equity; 003 is the most directly testable.
