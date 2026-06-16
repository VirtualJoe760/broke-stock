# Glossary

- **Backtest** — simulating a strategy on historical data with the live code path (see [parity](../01-architecture/engine-and-parity.md)).
- **Catalyst** — an event expected to re-rate a stock (earnings, M&A, policy, product).
- **Drawdown** — peak-to-trough decline; max drawdown is the worst observed.
- **Edge** — a repeatable, positive expected return after costs, distinct from leverage and luck.
- **Event study** — joining a signal to subsequent returns to test predictive power (validation L2).
- **Greeks** — option sensitivities: delta (price), theta (time decay), vega (volatility), gamma.
- **LEAPS** — long-dated options (~1yr+ expiry).
- **Lookahead / data leakage** — using information not available at decision time; for LLMs, includes training-cutoff leakage.
- **OTM** — out-of-the-money option (strike beyond current price); cheap, leveraged, can expire worthless.
- **Parity** — the property that backtest, paper, and live share one code path.
- **Point-in-time data** — data stored as it was known at each timestamp; required for honest backtests.
- **Sharpe / Sortino** — risk-adjusted return measures (Sortino penalizes only downside).
- **Surprise** — how much a signal deviates from what was already priced in; the alpha-bearing field.
- **Validation level (L0–L5)** — a strategy's place on the [validation ladder](../05-research/validation-methodology.md).
