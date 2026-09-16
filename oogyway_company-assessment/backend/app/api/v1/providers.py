from fastapi import APIRouter
from app.schemas.provider import ProviderStatusResponse
from app.services.llm.factory import get_llm_provider
from app.services.llm.ollama import OllamaProvider
from app.core.config import settings

router = APIRouter()


@router.get("/providers/status", response_model=ProviderStatusResponse)
async def get_provider_status():
    """Return current LLM provider, active model, health, and list of available providers."""
    provider = get_llm_provider()
    health = await provider.check_health()
    
    ollama_info = None
    if settings.LLM_PROVIDER.lower() == "ollama":
        ollama_info = health
    else:
        try:
            ollama_info = await OllamaProvider().check_health()
        except Exception:
            pass

    return ProviderStatusResponse(
        provider=provider.provider_name,
        model=provider.model_name,
        is_available=health.get("is_available", False),
        status_message=health.get("message", "Provider online"),
        available_providers=["ollama", "anthropic", "openai"],
        ollama_health=ollama_info
    )
