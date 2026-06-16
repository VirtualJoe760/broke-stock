# Regulatory & risk

> Status: drafted. Not legal advice — informs design; a securities attorney signs off before any live, third-party, or advertised use.

## The decisive question: whose money?

- **Personal account only** → minimal regulatory burden; most freedom.
- **Client money / advertised service / managing others** → the full weight of FINRA/SEC applies, and the architecture must be compliant by design.

This single fact drives autonomy, disclosures, and recordkeeping. Default to the stricter posture so personal use is a safe subset.

## What applies (when client money / a service is involved)

AI gets no special rulebook — FINRA's technology-neutral rules apply to it:

- **FINRA Rule 3110 (Supervision)** — written supervisory procedures governing the AI system. "The model decided" is not a defense.
- **Reg BI / suitability** — any AI-driven recommendation to a client must meet best-interest obligations.
- **Recordkeeping** — AI inputs/outputs/decisions (and generated audio) likely must be retained and reproducible.
- **"AI washing"** — the SEC has pursued firms overstating AI capabilities. Marketing claims must match reality. (Our headline-number skepticism is the same discipline applied to ourselves.)

FINRA flagged generative AI and agent-based risks in its 2025 and 2026 Oversight Reports.

## Risk controls that are also our compliance posture

- **PAPER / LIVE separation** — unmistakable in the UI; confirmation + (eventually) 2FA on live orders.
- **Validation gate** — capital is allocated only by [validation level](../05-research/validation-methodology.md). Untested strategies cannot reach real money. This is risk management *and* a supervisory control.
- **Hard risk gate** — position/exposure/loss limits + kill switch ([risk gate](../01-architecture/risk-gate.md)).
- **Voice/agent proposes, human approves** for live ([ADR-004](../00-overview/decisions-log.md)).
- **Full audit trail** — every decision, order, alert, and audio artifact logged and reconstructable.
- **Secrets management** — API keys in environment variables / secret stores, never committed to the repo or a `CLAUDE.md` ([ADR-008](../00-overview/decisions-log.md)). A reviewed source leaked an Alpaca key by committing it — exactly the failure to avoid.

## Instrument-specific risk

- **Options/LEAPS leverage** ([ADR-005](../00-overview/decisions-log.md)) — defined max loss (premium) but can go to zero; sizing must be total-loss-aware, and the risk gate matters *more*, not less.
- **Autonomous/24-7 agents** — an unsupervised agent compounds every failure mode; the safeguards list (position caps, daily-loss limits, trade-count caps, instrument bans) is mandatory before any autonomy.

## To detail

- Disclosure templates; recordkeeping retention policy; per-jurisdiction review
