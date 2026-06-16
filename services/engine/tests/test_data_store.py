"""Point-in-time store must never return data from the future (no lookahead)."""

from datetime import datetime, timezone

from broke_engine.data.store import MockPointInTimeStore


def test_point_in_time_no_lookahead() -> None:
    store = MockPointInTimeStore()
    start = datetime(2025, 2, 3, tzinfo=timezone.utc)
    end = datetime(2025, 3, 3, tzinfo=timezone.utc)
    as_of = datetime(2025, 2, 14, 23, 59, tzinfo=timezone.utc)

    bars = store.get_bars("TEST", start, end, as_of)

    assert bars, "expected some bars before as_of"
    assert all(b.ingest_ts <= as_of for b in bars), "no bar may be known after as_of"


def test_deterministic() -> None:
    store = MockPointInTimeStore()
    start = datetime(2025, 2, 3, tzinfo=timezone.utc)
    end = datetime(2025, 2, 28, tzinfo=timezone.utc)
    as_of = datetime(2025, 3, 1, tzinfo=timezone.utc)

    a = store.get_bars("NVDA", start, end, as_of)
    b = store.get_bars("NVDA", start, end, as_of)

    assert [x.close for x in a] == [x.close for x in b]
