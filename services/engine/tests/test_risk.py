"""Risk gate enforces hard limits and the kill switch."""

from broke_engine.risk import AccountState, OrderIntent, RiskGate, RiskLimits


def _account(**kw) -> AccountState:
    base = dict(equity=100_000.0, gross_exposure=0.0, day_pnl=0.0, new_positions_this_week=0)
    base.update(kw)
    return AccountState(**base)


def test_clean_order_approved() -> None:
    gate = RiskGate()
    d = gate.check(OrderIntent("NVDA", "buy", notional=4_000), _account())
    assert d.approved and not d.kill_switch


def test_oversized_position_rejected() -> None:
    gate = RiskGate()
    d = gate.check(OrderIntent("NVDA", "buy", notional=9_000), _account())  # 9% > 5%
    assert not d.approved


def test_options_blocked_by_default() -> None:
    gate = RiskGate()
    d = gate.check(OrderIntent("NVDA", "buy", notional=1_000, is_option=True), _account())
    assert not d.approved


def test_daily_loss_trips_kill_switch() -> None:
    gate = RiskGate()
    d = gate.check(OrderIntent("NVDA", "buy", notional=1_000), _account(day_pnl=-4_000))  # >3%
    assert d.kill_switch and not d.approved


def test_weekly_new_position_cap() -> None:
    gate = RiskGate()
    d = gate.check(OrderIntent("NVDA", "buy", notional=1_000), _account(new_positions_this_week=3))
    assert not d.approved


def test_options_allowed_when_enabled() -> None:
    gate = RiskGate(RiskLimits(allow_options=True))
    d = gate.check(OrderIntent("NVDA", "buy", notional=1_000, is_option=True), _account())
    assert d.approved
