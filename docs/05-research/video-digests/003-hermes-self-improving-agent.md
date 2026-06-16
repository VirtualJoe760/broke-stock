# Digest 003 — self-improving agent (Hermes + one-shot prompt)

- **Source:** YouTube — a "self-improving trading agent" built from a single copy-paste one-shot prompt, run in the Claude terminal, using the **Hermes** agent framework (pitched as a self-learning successor to OpenClaw), hosted on **Railway** 24/7.
- **Creator's challenge:** "10x challenge" — $50,000 → $500,000 in one year, **real money**, crypto.
- **No strategy-library entry extracted** — see "Why no strategy" below. The extraction is a *capability* + a design rubric: [self-improvement & optimization](../../01-architecture/self-improvement-and-optimization.md).

## What it is

A one-shot prompt that scaffolds and deploys an autonomous, **self-improving** trading agent:
- **Runtime:** Claude in the terminal (run with `--dangerously-skip-permissions`), deploying to **Railway** for 24/7 cloud execution.
- **Agent framework:** Hermes (self-learning); multi-agent — **Hermes** (portfolio mechanics, valuation weighting, weekly trade review) + **Cornelius** (filter thresholds, weekly parameter optimization, on a 3-day offset).
- **Strategy:** the creator's proprietary **"VACO Alpha"** momentum + yield strategy (~1.5M data points, run ~6–8 weeks), trading **real money** on crypto (BitTensor subnets), reordering every 30 minutes + daily.
- **Loop:** prompt → strategy → result → learn → improved strategy, running around the clock. First cycle is read-only verification before going live.

## The genuinely good idea — the 4-criteria rubric

The creator's framework for "a good agent" is sound and worth keeping:

1. **Accuracy** — precise, consistent input data; strong API connections; correct/objective conclusions (same input → same conclusion across agents).
2. **Reliability** — runs 24/7, survives the computer being off (cloud hosting).
3. **Defined goal** — define **success AND failure quantitatively** (target Sharpe, max drawdown, thresholds), within the realm of the possible.
4. **Self-improvement** — analyze results vs. target, hypothesize *why*, hypothesize *what next*, update via the **scientific method: change one variable at a time**, set a new baseline, iterate.

Defining *failure* explicitly and one-variable-at-a-time iteration are real best practices most retail attempts skip.

## Honest read

- **The concept is the holy grail; the video hand-waves the only hard part.** A self-improving agent that optimizes itself against its **own recent results will overfit / curve-fit** and can **reward-hack the metric** (Goodhart's law) — confidently optimizing its way into a blow-up. "Scientific method, one variable at a time" is necessary but **not sufficient**: every change must be tested on data it was *not* tuned on (walk-forward / out-of-sample), or the loop is just fitting noise. This is the central problem of self-improving trading agents, and it's exactly what our [validation ladder](../../05-research/validation-methodology.md) exists to contain.
- **Riskiest example we've reviewed.** Red flags: **real money from the start**; crypto; **30-minute trading** (intraday — contradicts [ADR-002](../../00-overview/decisions-log.md)); `--dangerously-skip-permissions` on a money-touching agent; a **black-box third-party framework** (Hermes) of unknown provenance as the brain; "completely free self-learning AI" is marketing (there is real cost); **10x/year (≈900%)** is a risk-of-ruin target, not an investment goal; a one-shot prompt that auto-installs and deploys to live trading is itself a security/operational hazard.
- **Net:** the strongest argument yet *for* validation-first. The self-improvement loop is a powerful capability that must run **inside** the framework — improve on in-sample, prove on an out-of-sample holdout, paper before live, with parameters **frozen** before any test window. Never let it rewrite itself on live capital.

## What we adopt vs. reject

**Adopt:**
- The **4-criteria rubric** as our agent-design checklist ([self-improvement & optimization](../../01-architecture/self-improvement-and-optimization.md)).
- **Quantitative success *and* failure** (target Sharpe, max drawdown, kill thresholds) — fold into the [strategy template](../../04-strategies/_TEMPLATE.md) and [risk gate](../../01-architecture/risk-gate.md).
- The **self-improvement loop as a gated capability** ([ADR-009](../../00-overview/decisions-log.md)): walk-forward / out-of-sample, no self-modification on live capital.
- The **read-only verification cycle before going live**.
- **Multi-agent separation of concerns** (portfolio mechanics vs. parameter optimization) as an optional pattern.

**Reject / gate:**
- Real-money-from-start, crypto, and **30-minute intraday** ([ADR-002](../../00-overview/decisions-log.md), [ADR-010](../../00-overview/decisions-log.md)).
- `--dangerously-skip-permissions` on anything that can move money.
- A black-box framework (Hermes) as our runtime — we control our own stack ([ADR-006](../../00-overview/decisions-log.md), [ADR-007](../../00-overview/decisions-log.md)).
- **Self-improvement without an out-of-sample gate** — the core danger.
- The 10x/year "goal" — it's a risk-of-ruin setting, not a target.

## Why no strategy-library entry

"VACO Alpha" is the creator's proprietary momentum+yield **crypto** strategy with no disclosed rules, on a 30-minute intraday cadence — outside our asset and horizon scope ([ADR-002](../../00-overview/decisions-log.md), [ADR-010](../../00-overview/decisions-log.md)). The transferable value is the *self-improvement capability* and the *agent rubric*, captured as architecture, not a tradeable strategy.
