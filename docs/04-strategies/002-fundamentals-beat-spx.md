# 002 — Fundamentals, beat the benchmark

- **ID:** 002
- **Status (validation level):** L0 — Hypothesis
- **Source:** [Digest 002 — 24/7 Claude Code Routines agent](../05-research/video-digests/002-claude-routines-24-7-agent.md)
- **Instruments:** Cash equities (no options — explicit safeguard)
- **Time horizon:** Long-term / swing (fundamentals-driven; not day trading)
- **Owner:** Joey
- **Last updated:** 2026-06-15

## Thesis (one sentence)

A fundamentals-driven, low-turnover equity portfolio, researched and rebalanced on a fixed schedule with disciplined risk safeguards, can beat the S&P 500 over time.

## Market regime assumptions

- **Needs:** nothing exotic — works in normal markets; long-term bias.
- **Breaks / risk:** "beating the index" in a single up month is usually just higher beta/concentration; the real test is risk-adjusted performance across an up year *and* a down/choppy year. Concentration is the hidden risk if safeguards slip.

## Rules

- **Universe / screen:** fundamentals-based selection (quality/value/catalyst). (Exact factors: TBD — must be made precise before L2.)
- **Entry:** planned during the pre-market research run; executed at open with a trailing stop (~10%).
- **Exit:** cut losers (~−7%), tighten stops on winners at midday; otherwise hold long-term.
- **Position sizing:** ≤5% per position; max ~3 new positions/week.
- **Risk controls:** daily loss limit; no options; explicit allowed/forbidden action list; paper-first.

## Claimed results (from source) + credibility read

| Claimed | Reality check |
|---|---|
| $10k, 30 days, beat S&P by ~8% (Opus 4.6) | **Unlevered equities — more sober than digest 001.** But one month, one account, single regime, no Sharpe/drawdown/sample. 8% over index in a month likely = beta/concentration in an up tape. |
| Runs 24/7 autonomously | Human reviews every run's transcript; safeguards constrain it. Effectively supervised, not unattended. |

## Validation log

| Level | Date | Result | Notes |
|---|---|---|---|
| L0 | 2026-06-15 | captured | from digest 002 |
| L1 | | pending | run logic check next |

## L1 logic-check questions (to answer next)

- Make the fundamental screen **precise and systematic** (which factors, what thresholds) so it's testable.
- Restate the +8% vs. the basket's **beta and concentration** — was it edge or just risk?
- Define the rebalance/exit rules deterministically (the trailing-stop and cut-loss numbers are a good start).
- How would this have done in a down/choppy month? Model the loss case.

## Open questions

- Is the edge in the *fundamental screen* (testable) or in the *agent's discretionary research* (hard to validate)? Only the former can climb the ladder.
- Does the schedule/rebalance cadence matter, or is it cosmetic? Test cadence as a parameter.

## Related strategies

[[001-leaps-catalyst-swing]] — both are swing/long-horizon; 001 adds options leverage, 002 is unlevered equity.
