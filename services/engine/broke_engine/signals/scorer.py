"""Score a news item into a validated Signal using the LLM provider.

This is the live "brain": text in -> structured Signal out. Requires a real
ANTHROPIC_API_KEY at call time (the module imports without one).
See docs/01-architecture/signal-layer.md.
"""

from __future__ import annotations

from ..llm.provider import LLMProvider
from .models import Signal, signal_json_schema

SYSTEM = (
    "You are a calibrated financial-news analyst. Given one news item about a stock, "
    "return a structured trading signal. The 'surprise' field is how much the news "
    "deviates from what is ALREADY priced in (0 = fully priced, 1 = total surprise) — "
    "this is the alpha-bearing field and matters more than raw sentiment. If you are "
    "uncertain, lower 'confidence'. Score only the named ticker; do not speculate beyond "
    "the item."
)


def score_news(provider: LLMProvider, ticker: str, headline: str, context: str = "") -> Signal:
    """Return a validated Signal for one news item. Raises on schema/validation failure."""
    user = f"Ticker: {ticker}\nHeadline: {headline}\n"
    if context:
        user += f"Context: {context}\n"
    result = provider.complete(SYSTEM, user, schema=signal_json_schema())
    if isinstance(result, dict):
        result.setdefault("ticker", ticker)  # guard: keep the asked-for ticker
    return Signal.from_dict(result)
