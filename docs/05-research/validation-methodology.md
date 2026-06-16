# Validation methodology

This document defines what "proven, tested results" means on this project. It is the most important document in the repo. Every strategy must climb this ladder; capital is allocated strictly by validation level.

## Why this exists

Trading ideas are cheap and almost all of them are wrong. The ones that look right are usually:
- **leverage masquerading as edge** (a 155% month from OTM options is a normal underlying move times leverage, not skill),
- **survivorship** (we only see the months/accounts that worked),
- **regime-dependent** (works in a bull tape, dies in a chop or a drawdown),
- **overfit** (tuned to the past, not the future),
- or **leaking the future** (especially with LLMs — see data-leakage below).

The job of this methodology is to **kill bad strategies cheaply** before they cost real money, and to graduate good ones with evidence.

## The validation ladder

A strategy has exactly one current level. It may only advance one level at a time, and only by meeting the promotion criteria. It can be demoted or killed at any level.

| Level | Name | What it means | Capital allowed |
|---|---|---|---|
| **L0** | Hypothesis | Captured from a video/idea/paper. Rules written down. Untested. | None |
| **L1** | Logic check | Survives scrutiny: edge is plausible, source caveats understood, leverage/regime/survivorship identified. | None |
| **L2** | Signal validation | The core signal predicts forward returns out-of-sample, after costs (cheap event study). | None |
| **L3** | Backtest | Full event-driven backtest: point-in-time data, realistic costs/slippage, no lookahead. Metrics meet thresholds. | None |
| **L4** | Paper / forward test | Live paper trading for ≥ a defined window; live results track backtest expectation. | Simulated |
| **L5** | Live (graduated) | Small real size, scaled up only as live results hold. | Real, capped |

**A strategy is only "proven" at L4+.** Until then it is, at best, "promising."

## Promotion criteria

**L0 → L1 (logic check).** Answer in writing:
- What is the claimed edge, in one sentence? Why should it exist (behavioral, structural, informational)?
- Is the claimed result driven by leverage? Restate returns un-levered.
- What market regime did it run in? Would it survive the opposite regime?
- Is the sample meaningful, or one account / one month?
- What would have to be true for this to be luck? How likely is that?

**L1 → L2 (signal validation / event study).** The cheap proof-of-edge, before building anything:
- Take the signal in isolation (e.g. "Claude sentiment surprise > 0.7", "oversold + catalyst").
- Join each signal to the *subsequent* return (1d / 1w / 1m), out-of-sample.
- Measure predictive power **after** transaction costs. If a single signal has no edge, nothing built on it will.
- Pass: positive, statistically non-trivial forward return after costs, on an out-of-sample window.

**L2 → L3 (backtest).** Full event-driven backtest meeting ALL of:
- Sharpe ≥ 1.0 (target; lower may pass with justification)
- Max drawdown within the strategy's stated risk budget
- Positive after realistic costs, slippage, and (for options) spread
- Holds across **at least two distinct market regimes** (e.g. an up year and a down/choppy year)
- No data-leakage red flags (see below)

**L3 → L4 (paper).** Forward paper-trade for a defined window (e.g. ≥ 8 weeks or ≥ N trades). Live paper results must track backtest expectation within tolerance — no large unexplained divergence (that divergence is usually the backtest lying).

**L4 → L5 (live).** Start at a small fixed dollar cap. Scale only as live P&L, slippage, and drawdown stay within the paper/backtest envelope. Any breach → demote.

## Required metrics (the scorecard every strategy reports)

- CAGR / period return **and** the same un-levered
- Sharpe and Sortino
- Max drawdown and time-to-recover
- Win rate, average win / average loss, profit factor
- Exposure (% time in market) and turnover
- Cost drag (commissions + slippage + spread as % of gross)
- Performance split by regime (bull / bear / chop)

A single headline return with none of the above is **not a result** — it's an anecdote.

## Anti-patterns we actively guard against

- **LLM data leakage.** Claude's training data includes the past. Backtesting an LLM strategy on dates *before* the model's training cutoff lets it "remember" outcomes. Mitigation: only backtest on data after the cutoff, or blind the model to anything post-decision-time. This is the single most dangerous trap for *this* project.
- **Lookahead bias.** Using any data point that wasn't actually available at decision time. Enforced by point-in-time storage with ingest timestamps.
- **Survivorship bias.** Exclude delisted names → inflated returns. Include them.
- **Transaction-cost denial.** Frictionless backtests print money. Always model costs, slippage, and spread.
- **Single-regime sampling.** A strategy validated only in a bull market is unvalidated.
- **Overfitting.** Too many parameters tuned on the same data. Prefer simple rules; reserve a true out-of-sample holdout.
- **Leverage confusion.** Always restate results un-levered before judging "edge."

## Self-improvement & walk-forward

Any adaptive / self-tuning strategy (see [self-improvement & optimization](../01-architecture/self-improvement-and-optimization.md), [ADR-009](../00-overview/decisions-log.md)) must be validated by **walk-forward**, never by fitting and testing on the same data:

- Optimize parameters on an **in-sample** window; change **one variable at a time**.
- **Freeze** parameters, then measure on an **out-of-sample** window the optimizer never saw.
- Promote only if the change holds out-of-sample and across regimes; that becomes the new baseline; repeat rolling forward.
- Beware **reward-hacking** the target metric (Goodhart): judge on multiple metrics together (return + drawdown + tail risk), not a single number.

A self-improving loop that tunes against its own recent (especially live) results is **overfitting by construction** and is treated as unvalidated.

## How a video becomes a tested strategy

1. Watch / transcribe → write a [video digest](video-digests/).
2. Extract the strategy into the [template](../04-strategies/_TEMPLATE.md) at **L0**.
3. Run the **L1 logic check** in the strategy file. Most ideas die here, on paper, for free.
4. Survivors get an **L2 event study**. Most of the rest die here.
5. Only the survivors justify the engineering cost of L3+.

This is the funnel that turns "I saw a guy make $100k" into either "we have evidence" or "we saved ourselves the loss."
