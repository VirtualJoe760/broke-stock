"""Alert rule evaluation + NoopDispatcher (no real sends)."""

from broke_engine.alerts import AlertRule, AlertType, NoopDispatcher, Tier, evaluate


def test_price_target_fires() -> None:
    rules = [AlertRule(AlertType.PRICE_TARGET, threshold=180, symbol="NVDA")]
    state = {"positions": [{"symbol": "NVDA", "last": 184.2}]}
    fired = evaluate(rules, state)
    assert len(fired) == 1 and fired[0].tier is Tier.NOTICE


def test_stop_fires_urgent() -> None:
    rules = [AlertRule(AlertType.STOP, threshold=210, symbol="AAPL")]
    state = {"positions": [{"symbol": "AAPL", "last": 205.0}]}
    fired = evaluate(rules, state)
    assert fired and fired[0].tier is Tier.URGENT


def test_daily_loss_critical() -> None:
    rules = [AlertRule(AlertType.DAILY_LOSS, threshold=3.0)]
    state = {"equity": 100_000, "day_pnl": -4_000}  # -4% > 3% limit
    fired = evaluate(rules, state)
    assert fired and fired[0].tier is Tier.CRITICAL


def test_signal_fires_on_high_confidence() -> None:
    rules = [AlertRule(AlertType.SIGNAL, threshold=0.7)]
    state = {"signals": [{"ticker": "MU", "confidence": 0.74}, {"ticker": "X", "confidence": 0.2}]}
    fired = evaluate(rules, state)
    assert len(fired) == 1 and fired[0].symbol == "MU"


def test_noop_dispatcher_records_no_send() -> None:
    d = NoopDispatcher()
    rules = [AlertRule(AlertType.PRICE_TARGET, threshold=180, symbol="NVDA")]
    for a in evaluate(rules, {"positions": [{"symbol": "NVDA", "last": 184.2}]}):
        d.dispatch(a)
    assert len(d.sent) == 1
