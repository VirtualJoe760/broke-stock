"""Market data models. `ingest_ts` = when the datum was known (point-in-time)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Bar:
    symbol: str
    ts: datetime  # bar close time
    open: float
    high: float
    low: float
    close: float
    volume: float
    ingest_ts: datetime  # when this bar became known — backtests filter on this
