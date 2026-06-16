"""Alert engine: rule evaluation + dispatch interface (Noop by default — no real sends)."""

from .dispatcher import AlertDispatcher, NoopDispatcher
from .engine import evaluate
from .models import Alert, AlertRule, AlertType, Tier

__all__ = ["Alert", "AlertRule", "AlertType", "Tier", "evaluate", "AlertDispatcher", "NoopDispatcher"]
