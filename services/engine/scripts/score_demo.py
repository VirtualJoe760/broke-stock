"""Smoke-test the live brain: score one headline into a Signal via Claude.

Requires ANTHROPIC_API_KEY (in the environment or services/engine/.env).
Run from services/engine:  python scripts/score_demo.py
"""

from broke_engine.llm import get_provider
from broke_engine.signals import score_news


def main() -> None:
    provider = get_provider()
    signal = score_news(
        provider,
        "NVDA",
        "Taiwan chip exports beat estimates, signaling resilient AI demand",
        context="Stock up ~3% pre-market; prior guidance already strong.",
    )
    print(signal)


if __name__ == "__main__":
    main()
