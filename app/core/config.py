from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Life Agent"
    GOOGLE_API_KEY: str
    DATABASE_URL: str
    DEBUG: bool = False  # Set to True in .env for development

    class Config:
        env_file = ".env"

settings = Settings()
