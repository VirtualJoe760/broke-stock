"""Analyst upgrade/downgrade events from FMP (stable /grades endpoint, free tier).

A clean, dated catalyst stream: each row has date, gradingCompany, previousGrade,
newGrade, and action (upgrade/downgrade/maintain/initiate). We keep only upgrades and
downgrades as directional events. Requires FMP_API_KEY.
"""

from __future__ import annotations

from datetime import datetime, timezone

import httpx

from ..config import settings


def fetch_grade_changes(
    symbol: str,
    start: datetime,
    end: datetime,
    api_key: str | None = None,
    timeout: float = 20.0,
) -> list[tuple[datetime, int, str]]:
    """Return (date, direction, label) for upgrades (+1) / downgrades (-1) in [start, end]."""
    api_key = api_key or settings.fmp_api_key
    url = f"https://financialmodelingprep.com/stable/grades?symbol={symbol}&apikey={api_key}"
    resp = httpx.get(url, timeout=timeout)
    if resp.status_code != 200:
        # Never surface the URL/key in the error (FMP carries the key in the query string).
        raise RuntimeError(f"FMP grades {symbol}: HTTP {resp.status_code}")
    out: list[tuple[datetime, int, str]] = []
    for x in resp.json() or []:
        action = (x.get("action") or "").lower()
        d = x.get("date")
        if action not in ("upgrade", "downgrade") or not d:
            continue
        try:
            dt = datetime.fromisoformat(d[:10]).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
        if start <= dt <= end:
            direction = 1 if action == "upgrade" else -1
            label = f"{x.get('gradingCompany')}: {x.get('previousGrade')}->{x.get('newGrade')}"
            out.append((dt, direction, label))
    return out
