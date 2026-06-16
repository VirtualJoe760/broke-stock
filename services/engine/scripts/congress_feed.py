"""Show the most recent congressional stock trades (the 'follow the smart money' feed).

Requires FMP_API_KEY. Run from services/engine: python scripts/congress_feed.py
"""

from __future__ import annotations

from broke_engine.data.congress import fetch_congress_trades


def main() -> None:
    trades = fetch_congress_trades(limit=100)
    buys = [t for t in trades if t.transaction_type == "buy"]
    print(f"{len(trades)} recent congressional stock trades fetched. Latest 15 PURCHASES:")
    for t in buys[:15]:
        print(f"  {t.disclosure_date}  {t.member:22} ({t.chamber:6}) BUY  {t.symbol:6} {t.amount}")


if __name__ == "__main__":
    main()
