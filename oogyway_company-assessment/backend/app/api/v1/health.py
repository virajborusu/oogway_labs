from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.db.session import get_db
from app.services.llm.factory import get_llm_provider

router = APIRouter()


@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    """Health check endpoint validating API, DB, and configured LLM provider status."""
    db_status = "healthy"
    try:
        await db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    provider = get_llm_provider()
    llm_health = await provider.check_health()

    return {
        "status": "ok" if db_status == "healthy" else "degraded",
        "service": "The Lenny Growth Assistant API",
        "database": db_status,
        "llm_provider": {
            "name": provider.provider_name,
            "model": provider.model_name,
            "details": llm_health
        }
    }


@router.get("/health/ollama")
async def ollama_health_check():
    """Specific health check for local Ollama service."""
    from app.services.llm.ollama import OllamaProvider
    ollama = OllamaProvider()
    return await ollama.check_health()
