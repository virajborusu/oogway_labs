import httpx
from typing import List, Dict, Any, Optional
from app.services.llm.base import LLMProvider
from app.core.config import settings
from app.core.logging import logger


class OllamaProvider(LLMProvider):
    def __init__(self, base_url: Optional[str] = None, model: Optional[str] = None):
        self.base_url = (base_url or settings.OLLAMA_BASE_URL).rstrip("/")
        self.model = model or settings.OLLAMA_MODEL

    @property
    def provider_name(self) -> str:
        return "ollama"

    @property
    def model_name(self) -> str:
        return self.model

    async def check_health(self) -> Dict[str, Any]:
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                res = await client.get(f"{self.base_url}/api/tags")
                if res.status_code == 200:
                    models = [m.get("name") for m in res.json().get("models", [])]
                    # Check if configured model or a variant exists
                    has_model = any(self.model in m for m in models)
                    return {
                        "is_available": True,
                        "status": "online",
                        "available_models": models,
                        "has_target_model": has_model,
                        "message": f"Ollama is running. Target model '{self.model}' is {'available' if has_model else 'missing (run: ollama pull ' + self.model + ')'}."
                    }
                return {
                    "is_available": False,
                    "status": "error",
                    "message": f"Ollama returned HTTP status {res.status_code}"
                }
        except Exception as e:
            return {
                "is_available": False,
                "status": "offline",
                "message": f"Cannot connect to Ollama at {self.base_url}. Ensure Ollama is installed and running (`ollama serve`). Details: {str(e)}"
            }

    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        health = await self.check_health()
        if not health["is_available"]:
            raise RuntimeError(health["message"])

        formatted_messages = []
        if system_prompt:
            formatted_messages.append({"role": "system", "content": system_prompt})
        formatted_messages.extend(messages)

        payload = {
            "model": self.model,
            "messages": formatted_messages,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            }
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                res = await client.post(f"{self.base_url}/api/chat", json=payload)
                if res.status_code == 404:
                    raise RuntimeError(f"Model '{self.model}' not found in Ollama. Run `ollama pull {self.model}`.")
                res.raise_for_status()
                data = res.json()
                return data.get("message", {}).get("content", "")
        except httpx.TimeoutException:
            logger.error("ollama_timeout", model=self.model)
            raise RuntimeError("Ollama model response timed out. Ensure the model is loaded properly.")
        except Exception as e:
            logger.error("ollama_error", error=str(e))
            raise RuntimeError(f"Ollama generation error: {str(e)}")
