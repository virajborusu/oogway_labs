import pytest
from app.services.llm.factory import get_llm_provider
from app.services.llm.ollama import OllamaProvider
from app.services.llm.anthropic import AnthropicProvider
from app.services.llm.openai import OpenAIProvider


@pytest.mark.asyncio
async def test_llm_provider_factory():
    ollama = get_llm_provider("ollama")
    assert ollama.provider_name == "ollama"

    anthropic = get_llm_provider("anthropic")
    assert anthropic.provider_name == "anthropic"

    openai = get_llm_provider("openai")
    assert openai.provider_name == "openai"


@pytest.mark.asyncio
async def test_anthropic_unconfigured_health():
    anthropic = AnthropicProvider(api_key="")
    health = await anthropic.check_health()
    assert health["is_available"] is False
    assert "missing" in health["message"].lower()


@pytest.mark.asyncio
async def test_openai_unconfigured_health():
    openai = OpenAIProvider(api_key="")
    health = await openai.check_health()
    assert health["is_available"] is False
    assert "missing" in health["message"].lower()
