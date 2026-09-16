from typing import Optional, List
from pydantic import BaseModel


class ProviderStatusResponse(BaseModel):
    provider: str
    model: str
    is_available: bool
    status_message: str
    available_providers: List[str]
    ollama_health: Optional[dict] = None
