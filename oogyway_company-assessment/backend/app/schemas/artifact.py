from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, ConfigDict


class ArtifactCreate(BaseModel):
    title: str
    artifact_type: Literal["markdown", "html"]
    content: str


class ArtifactResponse(BaseModel):
    id: str
    session_id: str
    message_id: Optional[str] = None
    title: str
    artifact_type: str
    content: str
    sanitized_content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
