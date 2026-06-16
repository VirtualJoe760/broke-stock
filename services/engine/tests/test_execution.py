"""Simulated matcher: slippage direction, commission, idempotency, position tracking."""

from broke_engine.execution import Order, SimulatedMatcher


def test_buy_pays_up_sell_receives_less() -> None:
    m = SimulatedMatcher(slippage_bps=10)
    buy = m.submit(Order("c1", "NVDA", "buy", 10), ref_price=100.0)
    sell = m.submit(Order("c2", "NVDA", "sell", 10), ref_price=100.0)
    assert buy.price > 100.0
    assert sell.price < 100.0


def test_idempotent_no_double_fill() -> None:
    m = SimulatedMatcher()
    o = Order("dup", "AAPL", "buy", 5)
    f1 = m.submit(o, 200.0)
    f2 = m.submit(o, 999.0)  # resubmit same id, different price
    assert f1 is f2  # same cached fill
    assert m.positions()["AAPL"] == 5  # not 10


def test_commission_applied() -> None:
    m = SimulatedMatcher(commission_per_share=0.01)
    f = m.submit(Order("c", "MSFT", "buy", 100), 300.0)
    assert f.commission == 1.0


def test_positions_net() -> None:
    m = SimulatedMatcher()
    m.submit(Order("a", "T", "buy", 10), 20.0)
    m.submit(Order("b", "T", "sell", 4), 21.0)
    assert m.positions()["T"] == 6


def test_bad_inputs() -> None:
    m = SimulatedMatcher()
    import pytest

    with pytest.raises(ValueError):
        m.submit(Order("x", "T", "buy", 1), ref_price=0.0)
    with pytest.raises(ValueError):
        m.submit(Order("y", "T", "hold", 1), ref_price=10.0)
