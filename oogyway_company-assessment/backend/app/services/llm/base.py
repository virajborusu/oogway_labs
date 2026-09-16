from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, AsyncGenerator


class LLMProvider(ABC):
    """Abstract Base Class for LLM Providers (Ollama, Anthropic, OpenAI)."""

    @abstractmethod
    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        """Generate a complete text response asynchronously."""
        pass

    @abstractmethod
    async def check_health(self) -> Dict[str, Any]:
        """Check availability and status of the provider."""
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        pass

    @property
    @abstractmethod
    def model_name(self) -> str:
        pass
