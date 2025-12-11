from fastapi import APIRouter, Depends, HTTPException
from app.services.gemini_service import GeminiService
from app.schemas.chat import PromptRequest, AgentResponse

router = APIRouter()

# Dependency Provider
def get_gemini_service():
    return GeminiService()

@router.post("/chat", response_model=AgentResponse)
async def chat_with_agent(
    request: PromptRequest,
    service: GeminiService = Depends(get_gemini_service) # Injection ici
):
    try:
        response_text = await service.generate_response(request.text)
        return AgentResponse(response=response_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
