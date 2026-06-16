"""LLM access — a single swappable provider interface (see provider.py)."""

from .provider import LLMProvider, get_provider

__all__ = ["LLMProvider", "get_provider"]
