# Strategy library

Every trading idea we evaluate lives here as a numbered strategy file, with a single current [validation level](../05-research/validation-methodology.md). Capital is allocated strictly by level. Nothing is "proven" below L4.

## Registry

| ID | Strategy | Horizon | Instruments | Status | Source |
|---|---|---|---|---|---|
| [001](001-leaps-catalyst-swing.md) | LEAPS + catalyst swing | Swing / 1yr+ LEAPS | LEAPS, small-cap equity | **L0** — Hypothesis | [Brandon (Robinhood)](../05-research/video-digests/001-brandon-claude-robinhood.md) |
| [002](002-fundamentals-beat-spx.md) | Fundamentals, beat the benchmark | Long-term / swing | Cash equities | **L0** — Hypothesis | [Routines 24/7 agent](../05-research/video-digests/002-claude-routines-24-7-agent.md) |
| [003](003-the-wheel-options-income.md) | The wheel (options income) | Swing / option cycles | Options (CSP + CC) | **L0** — Hypothesis | [Hermes Telegram analyst](../05-research/video-digests/004-hermes-telegram-analyst.md) |

## Status legend

- **L0** Hypothesis · **L1** Logic check · **L2** Signal validated · **L3** Backtested · **L4** Paper-proven · **L5** Live
- See the [validation ladder](../05-research/validation-methodology.md) for promotion criteria.

## Adding a strategy

1. Copy [`_TEMPLATE.md`](_TEMPLATE.md) to `NNN-short-name.md`.
2. Fill it from the source (usually a [video digest](../05-research/video-digests/)).
3. Add a row here at L0.
4. Run the L1 logic check in the strategy file. Advance only by meeting promotion criteria.
