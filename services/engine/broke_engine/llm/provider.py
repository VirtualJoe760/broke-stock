"""Swappable LLM provider interface.

The rest of the engine depends only on `LLMProvider`. Provider choice is config
(ADR-011): Anthropic API by default; an OpenAI-compatible endpoint (local Ollama/vLLM
on the Mac mini) for optional cheap triage. Switching is a base_url + model change.

See docs/08-deployment/model-hosting.md and docs/01-architecture/signal-layer.md.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from ..config import settings


class LLMProvider(ABC):
    """Minimal interface every provider implements."""

    @abstractmethod
    def complete(self, system: str, user: str, *, schema: dict[str, Any] | None = None) -> Any:
        """Return text, or a validated object when `schema` (a JSON schema) is given.

        Structured output is forced via tool-use so callers never parse prose
        (see signal-layer.md).
        """
        raise NotImplementedError


class AnthropicProvider(LLMProvider):
    """Claude via the Anthropic API. Default provider."""

    def __init__(self, model: str, api_key: str | None) -> None:
        self.model = model
        self._api_key = api_key
        # Client is constructed lazily so the engine imports without a key present
        # (paper/mock work needs no key).
        self._client: Any = None

    def _client_or_create(self) -> Any:
        if self._client is None:
            import anthropic  # imported lazily so the engine loads without the SDK/key

            # api_key=None lets the SDK read ANTHROPIC_API_KEY from the environment.
            self._client = anthropic.Anthropic(api_key=self._api_key)
        return self._client

    def complete(self, system: str, user: str, *, schema: dict[str, Any] | None = None) -> Any:
        client = self._client_or_create()
        # Cache the (static) system block to cut cost on repeated calls.
        system_blocks = [{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}]
        messages = [{"role": "user", "content": user}]

        if schema is None:
            msg = client.messages.create(
                model=self.model, max_tokens=1024, system=system_blocks, messages=messages
            )
            return "".join(b.text for b in msg.content if getattr(b, "type", None) == "text")

        # Structured output: force a single tool call whose input matches `schema`.
        tool = {"name": "emit", "description": "Return the structured result.", "input_schema": schema}
        msg = client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=system_blocks,
            messages=messages,
            tools=[tool],
            tool_choice={"type": "tool", "name": "emit"},
        )
        for b in msg.content:
            if getattr(b, "type", None) == "tool_use" and b.name == "emit":
                return b.input
        raise RuntimeError("model did not call the 'emit' tool")


class OpenAICompatibleProvider(LLMProvider):
    """Any OpenAI-compatible endpoint (local Ollama/vLLM) — used for optional triage."""

    def __init__(self, model: str | None, base_url: str | None, api_key: str | None) -> None:
        self.model = model
        self.base_url = base_url
        self._api_key = api_key

    def complete(self, system: str, user: str, *, schema: dict[str, Any] | None = None) -> Any:
        raise NotImplementedError(
            "OpenAICompatibleProvider.complete is a Phase-1 stub. Implement against an "
            "OpenAI-compatible /chat/completions endpoint."
        )


def get_provider() -> LLMProvider:
    """Construct the configured provider. Provider is chosen by env (ADR-011)."""
    provider = settings.llm_provider.lower()
    if provider == "anthropic":
        return AnthropicProvider(model=settings.llm_model, api_key=settings.anthropic_api_key)
    if provider == "openai-compatible":
        return OpenAICompatibleProvider(
            model=settings.triage_model,
            base_url=settings.openai_compatible_base_url,
            api_key=settings.openai_compatible_api_key,
        )
    raise ValueError(f"Unknown LLM_PROVIDER: {settings.llm_provider!r}")
