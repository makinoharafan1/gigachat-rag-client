from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class Agent(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    logo: Optional[str] = None
    system_prompt: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class AgentShortSchema(BaseModel):
    id: int
    title: str
    logo: str
