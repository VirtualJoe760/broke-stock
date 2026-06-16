# broke

An **AI trading-augmentation platform**: Claude turns unstructured market information (news, filings, analyst actions) into scored signals and a daily digest; two dashboards + alerts keep a human in the loop; deterministic code handles sizing, risk, and execution; and a **validation engine** tests every idea before a dollar is risked — the same engine runs identically in backtest, paper, and live.

**Honest positioning ([ADR-014](docs/00-overview/decisions-log.md)):** preliminary edge tests found **no tradeable alpha in the easy, freely-available signals** ([edge findings](docs/05-research/edge-findings.md)) — as expected from efficient markets and the LLM-trading literature. So this product's value is **augmentation** — faster research, monitoring, and disciplined process — **not** "AI that beats the market." It does not promise alpha; it refuses to risk money on anything unvalidated.

## Guiding principles

1. **One engine, three modes.** Backtest → paper → live share one code path (clock, data source, and venue are the only things that swap). See [decisions-log](docs/00-overview/decisions-log.md).
2. **Validation before capital.** No strategy touches real money before it clears the [validation ladder](docs/05-research/validation-methodology.md). One good month is not proof.
3. **Claude reasons; code decides risk.** The LLM scores meaning. Position sizing, limits, and the kill switch are deterministic.
4. **Swing / event-driven, not day trading.** The documented edge lives at the days-to-weeks (and LEAPS) horizon, not intraday scalping. See [ADR-002](docs/00-overview/decisions-log.md).
5. **Human-in-the-loop first.** Autopilot is a destination reached only after paper-proven results.

## Where to start

- [System overview](docs/00-overview/system-overview.md) — the whole thing in one read
- [Validation methodology](docs/05-research/validation-methodology.md) — how "proven" is defined
- [Strategy library](docs/04-strategies/README.md) — the catalog of hypotheses and their test status
- [Roadmap / phasing](docs/07-roadmap/phasing.md)

## Status

Pre-build. Documentation and strategy-research phase. No code, no capital.
