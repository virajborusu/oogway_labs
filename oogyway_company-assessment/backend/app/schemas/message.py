from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict, Field


class SourceItem(BaseModel):
    title: str
    source: str
    speaker: Optional[str] = None
    episode_url: Optional[str] = None
    snippet: str
    relevance_score: Optional[float] = None


class MessageCreate(BaseModel):
    content: str = Field(..., min_length=1, description="Message text cannot be empty")
    skill_override: Optional[str] = Field(None, description="Optional skill override ('ship_30_for_30' or 'artifact')")


class MessageResponse(BaseModel):
    id: str
    session_id: str
    role: str
    content: str
    sources: Optional[List[SourceItem]] = None
    created_at: datetime
    meta_info: Optional[Dict[str, Any]] = None
    artifact_id: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
