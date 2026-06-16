"""Congressional trade disclosures (FMP senate-latest + house-latest, free tier).

A "follow the smart money" feed. Each disclosure has the symbol, member, buy/sell,
amount range, and BOTH the transaction date and the (later) disclosure date — the
disclosure date is the only date you could actually act on. Requires FMP_API_KEY.
"""

from __future__ import annotations

from dataclasses import dataclass

import httpx

from ..config import settings

_BASE = "https://financialmodelingprep.com/stable"


@dataclass(frozen=True)
class CongressTrade:
    symbol: str
    member: str
    chamber: str  # "senate" | "house"
    transaction_type: str  # "buy" | "sell" | "other"
    disclosure_date: str  # actionable date (filed after the trade)
    transaction_date: str
    amount: str
    link: str


def _norm_type(t: str | None) -> str:
    s = (t or "").lower()
    if "purchase" in s or s == "buy":
        return "buy"
    if "sale" in s or "sold" in s or s == "sell":
        return "sell"
    return "other"


def fetch_congress_trades(limit: int = 100, api_key: str | None = None, timeout: float = 20.0) -> list[CongressTrade]:
    api_key = api_key or settings.fmp_api_key
    limit = min(limit, 25)  # FMP free tier caps 'limit' at 25
    out: list[CongressTrade] = []
    for chamber, ep in (("senate", "senate-latest"), ("house", "house-latest")):
        r = httpx.get(f"{_BASE}/{ep}?page=0&limit={limit}&apikey={api_key}", timeout=timeout)
        if r.status_code != 200:
            continue
        for x in r.json() or []:
            sym = x.get("symbol")
            if not sym or (x.get("assetType") or "").lower() != "stock":
                continue
            out.append(
                CongressTrade(
                    symbol=sym,
                    member=f"{x.get('firstName', '')} {x.get('lastName', '')}".strip(),
                    chamber=chamber,
                    transaction_type=_norm_type(x.get("type")),
                    disclosure_date=x.get("disclosureDate", ""),
                    transaction_date=x.get("transactionDate", ""),
                    amount=x.get("amount", ""),
                    link=x.get("link", ""),
                )
            )
    out.sort(key=lambda t: t.disclosure_date, reverse=True)
    return out
