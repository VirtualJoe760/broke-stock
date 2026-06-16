# Signal / intelligence layer (Claude)

## Responsibility

Turn unstructured text (news, filings, transcripts) into typed, scored signals. This is the part Claude is genuinely good at — meaning, not speed.

## Signal schema

Forced structured output (tool/JSON schema) — never parse prose:

```json
{
  "ticker": "NVDA",
  "event_type": "guidance_raise | downgrade | mna | litigation | ...",
  "sentiment": -1.0,
  "surprise": 0.0,
  "magnitude": "minor | moderate | major",
  "time_horizon": "intraday | days | weeks",
  "confidence": 0.0,
  "rationale": "one line"
}
```

`surprise` (deviation from what's priced in) is the alpha-bearing field, not raw sentiment.

## Model tiering (cost + the Mac-mini option)

- **Triage:** a small/cheap model classifies the firehose (relevant? which tickers?). Optionally a local model on the Mac mini via Ollama ([model hosting](../08-deployment/model-hosting.md)).
- **Deep read:** items that pass triage go to Claude (Sonnet/Opus) for the structured signal.
- **Prompt caching** on the static instruction block keeps cost down at scale.

## The 4-layer daily reference design

Adapted from [digest 001](../05-research/video-digests/001-brandon-claude-robinhood.md):

1. **Data + valuation** — prices, option chains, compute Greeks, save snapshot, P/L vs. target.
2. **Portfolio analysis** — exposure by name/sector, aggregate Greeks, IV, theta decay.
3. **Market + news** — macro gate (VIX, breadth, credit spreads) + per-position news scoring.
4. **Integration** — diff vs. yesterday, fire alerts, render outputs.

## Entity resolution

Map names → tickers; handle collisions and **second-order effects** (a TSMC headline moves NVDA). A bad mapping silently corrupts every downstream signal.

## Critical risk — LLM data leakage

Claude's training data includes the past. Backtesting an LLM strategy on dates *before* the model's cutoff lets it "remember" outcomes. Mitigate by testing only on post-cutoff data, or blinding the model to anything after decision time. This is the most dangerous trap specific to this project — see [validation methodology](../05-research/validation-methodology.md).

## Single source of truth

The agent's prompts/skills reference the validated [strategy specs](../04-strategies/README.md) and a persistent `CLAUDE.md`-style spec ([ADR-008](../00-overview/decisions-log.md)) — the signal layer does not invent edge or self-modify live parameters ([ADR-009](../00-overview/decisions-log.md)).

## Open questions

- Final prompt set + schema versioning.
- Triage model choice + relevance threshold to control deep-read spend.
