from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Smart Campus Multi-Agent AI System"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "sqlite:///./smart_campus.db"
    
    # JWT Auth
    SECRET_KEY: str = "SUPER_SECRET_KEY_CHANGE_ME_IN_PRODUCTION_1234567890"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # OpenAI API / LLM Configuration
    OPENAI_API_KEY: Optional[str] = None
    
    model_config = ConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()
