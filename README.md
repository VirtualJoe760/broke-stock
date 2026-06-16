# broke

An AI-assisted equities research-and-execution platform. Claude turns unstructured market information (news, filings, transcripts) into scored, structured signals; deterministic code handles sizing, risk, and execution; and the same engine runs identically in backtest, paper, and live.

The product is not "AI that trades." The product is a **validation engine** that turns trading *ideas* into *proven, tested results* — and refuses to risk real money on anything that hasn't earned its way up the ladder.

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
