from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict


class SessionCreate(BaseModel):
    title: Optional[str] = "New Growth Conversation"
    meta_info: Optional[Dict[str, Any]] = None


class SessionResponse(BaseModel):
    id: str
    title: str
    created_at: datetime
    updated_at: datetime
    meta_info: Optional[Dict[str, Any]] = None
    message_count: Optional[int] = 0

    model_config = ConfigDict(from_attributes=True)
