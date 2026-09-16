from typing import List, Dict, Any, Optional

from app.services.llm.base import LLMProvider
from app.core.config import settings
from app.core.logging import logger


class AnthropicProvider(LLMProvider):
    """Anthropic provider backed by the Claude Agent SDK.

    The local demo still uses Ollama. This provider exists to satisfy the
    assessment's agent-layer requirement and provides a cloud path when an
    Anthropic API key is configured.
    """

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.ANTHROPIC_API_KEY
        self.model = model or settings.ANTHROPIC_MODEL

    @property
    def provider_name(self) -> str:
        return "anthropic"

    @property
    def model_name(self) -> str:
        return self.model

    async def check_health(self) -> Dict[str, Any]:
        if not self.api_key:
            return {
                "is_available": False,
                "status": "unconfigured",
                "message": "Anthropic API key is missing. Set ANTHROPIC_API_KEY in .env",
            }
        return {
            "is_available": True,
            "status": "configured",
            "message": f"Anthropic Agent SDK configured with model '{self.model}'",
        }

    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        if not self.api_key:
            raise RuntimeError("Anthropic API key is missing. Configure ANTHROPIC_API_KEY in .env")

        # The SDK reads ANTHROPIC_API_KEY from the environment. Temporarily set
        # it from application configuration so the provider also works when the
        # key was supplied through the app's .env/settings layer.
        import os
        os.environ.setdefault("ANTHROPIC_API_KEY", self.api_key)

        try:
            from claude_agent_sdk import AssistantMessage, ClaudeAgentOptions, TextBlock, query
        except ImportError as exc:
            raise RuntimeError(
                "Claude Agent SDK is not installed. Reinstall backend requirements."
            ) from exc

        history = "\n\n".join(
            f"{m['role'].upper()}: {m['content']}" for m in messages
        )
        prompt = (
            f"<conversation>\n{history}\n</conversation>\n\n"
            f"<system_instructions>\n{system_prompt or ''}\n</system_instructions>\n\n"
            "Answer the latest user request while respecting the supplied instructions."
        )

        try:
            options = ClaudeAgentOptions(
                model=self.model,
                system_prompt=system_prompt or "You are a helpful assistant.",
                max_turns=1,
                allowed_tools=[],
            )
            parts: List[str] = []
            async for message in query(prompt=prompt, options=options):
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            parts.append(block.text)
            result = "".join(parts).strip()
            if not result:
                raise RuntimeError("Anthropic Agent SDK returned an empty response")
            return result
        except Exception as exc:
            logger.error("anthropic_agent_sdk_error", error=str(exc))
            raise RuntimeError(f"Anthropic Agent SDK error: {exc}") from exc
