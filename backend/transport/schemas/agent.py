from pydantic import BaseModel

class AgentShortSchema(BaseModel):
    id: int
    title: str
    logo: str
