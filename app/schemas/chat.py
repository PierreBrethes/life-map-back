from pydantic import BaseModel

class PromptRequest(BaseModel):
    text: str

class AgentResponse(BaseModel):
    response: str
