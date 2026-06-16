# Edge findings (the honest record)

What the validation work actually found, so nobody re-litigates it or quietly forgets it.

## Tests run (June 2026)

| # | Signal | Data | Method | Result |
|---|---|---|---|---|
| 1 | Headline **surprise** | Polygon news + Claude scoring | L2 event study, catalyst-filtered, post-cutoff (Feb–May 2026), 46 events | **No edge.** Only 1/46 cleared a sensible surprise bar → no signal. |
| 2 | **Analyst revisions** | FMP grades (up/downgrades) + Polygon prices | Directional factor test, 15 events, 5-day fwd, cost-adjusted | **No edge.** Spread −4.14% (wrong way), t-stat −0.23 (noise). |

Both runs are committed and reproducible (`scripts/real_l2_v2.py`, `scripts/grade_l2.py`).

## Interpretation

- **Two plausible, freely-available signals → two nulls.** Consistent with efficient markets: widely-watched information is already priced in.
- This matches the credible literature we reviewed at the outset (LLMs are strong as **augmentation**, weak as autonomous **alpha**) and the StockBench finding that LLM agents rarely beat a passive baseline.
- **We did not fool ourselves.** The naive path — wire the autopilot, catch a lucky paper week, declare victory — is exactly what the validation ladder exists to prevent. It worked.

## Honest caveats

- Small samples, free-tier data, single post-cutoff window. These are **preliminary**, not a definitive "no edge ever."
- A larger/paid study *could* be run, but the base rate says it most likely confirms the null.

## Decision

Re-scope the product's core value from **alpha generation** to **augmentation** — see [ADR-014](../00-overview/decisions-log.md). Edge hunting continues only as cheap, opt-in experiments via the harness; the product no longer *depends* on beating the market.
