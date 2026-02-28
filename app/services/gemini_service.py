import google.generativeai as genai
from app.core.config import settings

class GeminiService:
    def __init__(self):
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)

    async def generate_response(self, prompt: str) -> str:
        # The call is asynchronous to avoid blocking the server
        # Note: google-generativeai may not be fully async native in all versions, 
        # but wrapping in a thread or using async methods if provided is key. 
        # The library now supports async methods.
        response = await self.model.generate_content_async(prompt)
        return response.text
