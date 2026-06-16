"""Point-in-time data store.

The non-negotiable rule (see docs/01-architecture/data-and-ingestion.md and the
validation methodology): a query may only return data whose `ingest_ts <= as_of`.
This is what prevents lookahead/data-leakage in backtests.

`MockPointInTimeStore` generates deterministic synthetic data so the whole pipeline
runs with no API keys and no real data. `DuckDBPointInTimeStore` is the real store
(Phase 1+) over Parquet/DuckDB.
"""

from __future__ import annotations

import random
from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone

from .models import Bar


class PointInTimeStore(ABC):
    @abstractmethod
    def get_bars(self, symbol: str, start: datetime, end: datetime, as_of: datetime) -> list[Bar]:
        """Daily bars in [start, end] known as of `as_of` (ingest_ts <= as_of). No lookahead."""
        raise NotImplementedError


class MockPointInTimeStore(PointInTimeStore):
    """Deterministic synthetic daily bars (seeded random walk). Weekdays only.

    Each bar's ingest_ts == its close time, so `as_of` enforces point-in-time access.
    Deterministic per (seed, symbol) so backtests are reproducible.
    """

    def __init__(self, seed: int = 42, start_price: float = 100.0) -> None:
        self._seed = seed
        self._start_price = start_price

    def _series(self, symbol: str, start: datetime, end: datetime) -> list[Bar]:
        rng = random.Random(f"{self._seed}:{symbol}")
        bars: list[Bar] = []
        price = self._start_price
        day = start
        while day <= end:
            if day.weekday() < 5:  # Mon–Fri
                drift = rng.uniform(-0.020, 0.022)  # slight upward bias
                o = price
                c = max(1.0, o * (1 + drift))
                hi = max(o, c) * (1 + rng.uniform(0, 0.01))
                lo = min(o, c) * (1 - rng.uniform(0, 0.01))
                vol = rng.uniform(1e6, 5e6)
                ts = day.replace(hour=20, minute=0, second=0, microsecond=0, tzinfo=timezone.utc)
                bars.append(
                    Bar(
                        symbol=symbol,
                        ts=ts,
                        open=round(o, 2),
                        high=round(hi, 2),
                        low=round(lo, 2),
                        close=round(c, 2),
                        volume=round(vol),
                        ingest_ts=ts,
                    )
                )
                price = c
            day += timedelta(days=1)
        return bars

    def get_bars(self, symbol: str, start: datetime, end: datetime, as_of: datetime) -> list[Bar]:
        return [b for b in self._series(symbol, start, end) if b.ingest_ts <= as_of]


class DuckDBPointInTimeStore(PointInTimeStore):
    """Real store over Parquet/DuckDB (Phase 1+). Query filters `ingest_ts <= as_of`."""

    def __init__(self, path: str) -> None:
        self.path = path

    def get_bars(self, symbol: str, start: datetime, end: datetime, as_of: datetime) -> list[Bar]:
        raise NotImplementedError(
            "DuckDBPointInTimeStore is a Phase-1 stub; use MockPointInTimeStore for offline work. "
            "Real impl: SELECT ... WHERE symbol = ? AND ts BETWEEN ? AND ? AND ingest_ts <= ?"
        )
