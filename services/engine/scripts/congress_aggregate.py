"""Aggregate recent congressional trades: most-active members, cross-member consensus,
and a named-member filter (e.g. Pelosi). Requires FMP_API_KEY. Run from services/engine.
"""

from __future__ import annotations

from broke_engine.data.congress import (
    aggregate_by_member,
    consensus_buys,
    fetch_congress_trades,
    trades_for_member,
)


def main() -> None:
    trades = fetch_congress_trades(limit=25, pages=4)
    print(f"{len(trades)} recent congressional stock trades (paged).")

    by = aggregate_by_member(trades)
    active = sorted(by.items(), key=lambda kv: -(len(kv[1]["buys"]) + len(kv[1]["sells"])))[:8]
    print("\nMost active members (recent window):")
    for m, d in active:
        print(f"  {m:24} {len(d['buys'])} buys / {len(d['sells'])} sells")

    print("\nConsensus buys (>= 2 distinct members):")
    cons = consensus_buys(trades, min_members=2)
    if cons:
        for sym, n, members in cons[:12]:
            print(f"  {sym:6} {n} members: {', '.join(members)}")
    else:
        print("  (none in this window)")

    for name in ["Pelosi", "Khanna"]:
        mt = trades_for_member(trades, name)
        print(f"\n{name}: {len(mt)} recent trades")
        for t in mt[:6]:
            print(f"  {t.disclosure_date} {t.transaction_type.upper():4} {t.symbol} {t.amount}")


if __name__ == "__main__":
    main()
