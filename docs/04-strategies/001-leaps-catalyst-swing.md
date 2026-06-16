# 001 — LEAPS + catalyst swing

- **ID:** 001
- **Status (validation level):** L0 — Hypothesis
- **Source:** [Brandon — Claude + Robinhood, May challenge](../05-research/video-digests/001-brandon-claude-robinhood.md)
- **Instruments:** Long-dated OTM call options (LEAPS, ~1yr+ expiry) on liquid large-caps; cash equity on researched small-caps
- **Time horizon:** Swing to position (weeks–months); LEAPS held toward a 1yr+ directional thesis
- **Owner:** Joey
- **Last updated:** 2026-06-15

## Thesis (one sentence)

Oversold, fundamentally-sound names with a clear re-rating catalyst tend to mean-revert upward over weeks–months, and expressing that view through long-dated OTM calls converts a moderate underlying move into an outsized return while capping downside at the premium.

## Market regime assumptions

- **Needs:** a neutral-to-rising tape and live catalysts (post-earnings dislocation, government support, sector momentum). Works best when implied volatility on the chosen options is *reasonably priced*.
- **Breaks in:** sustained risk-off / drawdown regimes (OTM calls decay to zero), volatility spikes that inflate premiums, or stock-specific catalysts that fail to materialize. The May result ran in a strong bull month — the opposite regime is the real test.

## Rules

- **Universe / screen:** liquid large-caps with reasonably-priced options for the LEAPS sleeve; thoroughly-researched small-caps (held as equity, *not* options — small-cap option chains are illiquid/expensive) for the second sleeve. Candidates scored on catalyst timing, IV environment, and market correlation.
- **Entry:** stock is oversold/undervalued with an identifiable catalyst to re-rate (e.g. clean post-earnings drop). For LEAPS: OTM strike, ≥45 days to expiry (Brandon used ~1yr+), chosen by Greeks (theta/delta) and premium vs. IV.
- **Exit:** target on the catalyst playing out; cut on thesis invalidation; manage theta decay as expiry approaches. (Exact target/stop rules: TBD — must be made precise before L2.)
- **Position sizing:** diversify across sectors (healthcare, AI infra, enterprise software …) and across catalyst horizons (short / medium / long) so no single earnings event dominates. (Exact sizing rule: TBD.)
- **Risk controls:** per-position premium cap; concentration limit per name/sector; the LEAPS sleeve is inherently high-variance, so the deterministic risk gate matters MORE here, not less.

## Claimed results (from source) + credibility read

| Claimed | Reality check |
|---|---|
| $66k → ~$169k, +155% in May 2026 (~$102k gain) | **Leverage + regime, not demonstrated edge.** OTM LEAPS turn a ~15–25% underlying move into 100%+ option returns; May was strongly risk-on and the names (HIMS, OSCR, MP, NOW, Nokia) all ran. |
| "Claude managed the portfolio" | Human-in-the-loop: operator (a quant — UCLA math/econ, ex-Raymond James) chose trades; Claude researched + monitored; trades placed manually on Robinhood. |
| Repeatable method | One account, one month, no drawdown / Sharpe / sample disclosed. Un-levered and across regimes is unknown. The same structure can lose 40–70% in a bad month (options → 0). |

## Validation log

| Level | Date | Result | Notes |
|---|---|---|---|
| L0 | 2026-06-15 | captured | from Brandon video digest |
| L1 | | pending | run logic check next |

## L1 logic-check questions (to answer next)

- Restate the result **un-levered**: what did the underlying basket actually do in May?
- Define **precise** entry/exit/sizing rules (currently qualitative) so the strategy is testable.
- Is the edge the *stock selection* (oversold + catalyst) or the *options structuring* (leverage)? These must be validated separately — leverage is not edge.
- What does this do in a down/choppy month? Model the loss case explicitly.

## Open questions

- Does the "oversold + clear catalyst" screen have standalone forward-return edge (L2 event study) *before* any options leverage is applied?
- How much of the return is Claude's research vs. the operator's quant judgment? Can the screen be made systematic enough to test without a quant in the loop?

## Related strategies

(none yet)
