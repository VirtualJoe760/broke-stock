# Digest 001 — Brandon: Claude + Robinhood, May challenge

- **Source:** YouTube — "I Tested Letting Claude Trade For A Month and Made $102k" (creator: Brandon; runs a Skool AI-trading community)
- **Creator background:** UCLA math/economics; ~3 years investment banking at Raymond James. A quant. This matters — see honest read.
- **Account:** new Robinhood account, deposited ~$66k early May → ~$169k end of May (≈155% / ~$102k gain).
- **Extracted strategy:** [001 — LEAPS + catalyst swing](../../04-strategies/001-leaps-catalyst-swing.md)

## What he actually built

A **human-in-the-loop** system in two phases. Claude researched and monitored; he chose and placed the trades on Robinhood.

He distinguishes two ways he uses Claude:
- **Deterministic** — Claude writes code for fixed-rule systems wired to an API-first broker (IBKR/Alpaca). (His usual approach; *not* the focus here.)
- **Non-deterministic** — Claude as an analyst giving qualitative answers. This challenge used **both**, and deliberately used Robinhood + the Claude web UI to show a low-cost, accessible setup.

### Phase 1 — Claude as research analyst (web UI)

- Fed Claude tight context (account size, risk tolerance, holding period); asked for a monthly strategy with **big upside, limited downside**.
- Resulting plan, two sleeves:
  1. **Long-dated OTM call options (LEAPS)** on large-caps with reasonably-priced options — leveraged directional bets; Greeks (theta/delta) watched to manage time decay; ≥45 days to expiry, in practice Jan-2027 expiries (~1yr+). Avoided short-dated options ("rely on perfect timing and luck").
  2. **Researched small-cap equities** — skipped small-cap options (illiquid, expensive premiums).
- Stock selection: oversold/undervalued names with a clear re-rating catalyst + upward momentum. Candidates discussed: OSCR, MBIS, ServiceNow (NOW), HIMS, MP, Nokia. Scored on catalyst timing, IV environment, market correlation. Diversified across sectors and catalyst horizons. Built probability distributions for option expected value (e.g. Nokia).
- Example trades: ServiceNow ~$120 strike and Nokia ~$20 strike, both Jan-2027, both OTM (aggressive leverage).

### Phase 2 — daily monitoring "options terminal" (~$1/day)

Built with Claude Code, connected to the Robinhood portfolio, run once each morning. Four layers, each a prompt building on the last:

1. **Data + valuation** — spot prices + full option chain for every holding; match owned contracts; compute Greeks locally (Yahoo Finance free, or premium like FMP); save daily snapshots; output P/L and proximity to target.
2. **Portfolio analysis** — exposure by stock/sector, aggregate Greeks, theta decay, IV environment, overall risk.
3. **Market + news** — a macro gate (VIX, credit spreads, market breadth) + Claude reading per-position news daily (sentiment, technicals). This is the token-spend layer.
4. **Integration** — diffs today vs. yesterday's snapshot to detect new strikes/expiries; fires target/stop and IV-change alerts; pushes to **Telegram/email**; renders the dashboard (net worth, notifications, theta-decay view, strike ladder, Greeks, macro gate, per-position news).

## Claimed results

+155% in May (~$66k → ~$169k). No drawdown, Sharpe, sample size, or un-levered figure disclosed. Explicit disclaimer: not financial advice, don't copy the specific trades (entry prices are period-specific).

## Honest read

- **The return is leverage × a hot month, not demonstrated edge.** OTM LEAPS convert a ~15–25% underlying move into 100%+ option returns; May 2026 was strongly risk-on and his picks ran hard. Same structure can lose 40–70% in a bad month (options decay to zero).
- **He's a quant.** The strike selection, Greek management, probability distributions, and catalyst diversification reflect real expertise expressed *through* Claude, not Claude replacing skill.
- **It's swing/position trading with 1yr+ options — not day trading, not autopilot.** Reinforces our documented default (see [ADR-002](../../00-overview/decisions-log.md)).

## What we adopt vs. reject

**Adopt:**
- The **two-dashboard split** (content/news analysis + trader/options terminal) — matches our design.
- The **daily Claude analyst run + snapshot-diffing + Telegram/email alerts** — concrete reference for our signal + alert layers.
- **Cost discipline** — once-daily run (~$1/day), web subscription for research before paying for API.
- **Options/LEAPS + Greeks monitoring** as a first-class strategy class ([ADR-005](../../00-overview/decisions-log.md)).
- The **4-layer daily-monitoring prompt structure** as a documented reference design.

**Reject / gate:**
- The headline number as evidence of anything. It enters our system as a **hypothesis (L0)**, not a result.
- Unbounded leverage without a deterministic risk gate. LEAPS make our risk layer *more* important.
