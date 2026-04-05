from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    gemini_api_key: str
    tavily_api_key: str = ""
    langchain_api_key: str = ""
    api_key: str = "sk-dev-key-change-in-prod"

    environment: str = "development"
    redis_host: str  = "localhost"
    redis_port: int  = 6379

    llm_model:   str = "gemini-2.5-flash"
    embed_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    max_tokens:  int = 800
    rate_limit:  int = 20       # requests / minute per IP

    langchain_tracing_v2: str = "true"
    langchain_project: str    = "ai-api-prod"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()