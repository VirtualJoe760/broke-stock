"""The default provider is Anthropic and constructs without a key present (paper/mock)."""

from broke_engine.llm import get_provider
from broke_engine.llm.provider import AnthropicProvider


def test_default_provider_is_anthropic() -> None:
    provider = get_provider()
    assert isinstance(provider, AnthropicProvider)
    assert provider.model  # a model id is configured
