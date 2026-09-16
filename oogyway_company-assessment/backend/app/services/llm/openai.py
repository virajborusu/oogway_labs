import httpx
from typing import List, Dict, Any, Optional
from app.services.llm.base import LLMProvider
from app.core.config import settings
from app.core.logging import logger


class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.OPENAI_API_KEY
        self.model = model or settings.OPENAI_MODEL

    @property
    def provider_name(self) -> str:
        return "openai"

    @property
    def model_name(self) -> str:
        return self.model

    async def check_health(self) -> Dict[str, Any]:
        if not self.api_key:
            return {
                "is_available": False,
                "status": "unconfigured",
                "message": "OpenAI API key is missing. Set OPENAI_API_KEY in .env"
            }
        return {
            "is_available": True,
            "status": "ready",
            "message": f"OpenAI Provider configured with model '{self.model}'"
        }

    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        if not self.api_key:
            raise RuntimeError("OpenAI API key is missing. Configure OPENAI_API_KEY in .env")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        formatted_messages = []
        if system_prompt:
            formatted_messages.append({"role": "system", "content": system_prompt})
        formatted_messages.extend(messages)

        payload = {
            "model": self.model,
            "messages": formatted_messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        try:
            async with httpx.AsyncClient(timeout=45.0) as client:
                res = await client.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
                res.raise_for_status()
                data = res.json()
                choices = data.get("choices", [])
                if choices:
                    return choices[0].get("message", {}).get("content", "")
                return ""
        except Exception as e:
            logger.error("openai_error", error=str(e))
            raise RuntimeError(f"OpenAI API error: {str(e)}")
