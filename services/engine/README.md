# broke engine

Python service: signal scoring (Claude), strategy logic, risk gate, and execution — paper-first. Built on NautilusTrader for backtest↔live parity ([engine & parity](../../docs/01-architecture/engine-and-parity.md)).

## Layout (filling in)

```
broke_engine/
  config.py        # env-driven settings (no hardcoded secrets)
  llm/             # swappable LLM provider (Anthropic default; OpenAI-compatible for triage)
  data/            # point-in-time ingestion + stores (DuckDB/Parquet, QuestDB)   [Phase 1]
  signals/         # Claude structured-output signal scorer                        [Phase 1]
  strategies/      # deterministic, backtestable strategy logic                    [Phase 1+]
```

## Dev

```
pip install -e ".[dev]"      # add ".[engine]" for NautilusTrader
```

Runs in **paper/mock mode** with no API keys. Live trading requires explicit opt-in and supervision ([risk gate](../../docs/01-architecture/risk-gate.md)).
