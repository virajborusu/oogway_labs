from typing import Optional, Dict, Any, List
from app.services.llm.base import LLMProvider
from app.services.llm.ollama import OllamaProvider
from app.services.llm.anthropic import AnthropicProvider
from app.services.llm.openai import OpenAIProvider
from app.core.config import settings
from app.core.logging import logger



def get_llm_provider(provider_name: Optional[str] = None) -> LLMProvider:
    name = (provider_name or settings.LLM_PROVIDER).lower()

    if name == "ollama":
        return OllamaProvider()
    elif name == "anthropic":
        return AnthropicProvider()
    elif name == "openai":
        return OpenAIProvider()
    else:
        logger.warning("unknown_provider_requested", provider=name)
        return OllamaProvider()
