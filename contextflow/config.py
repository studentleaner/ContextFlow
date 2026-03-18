from pydantic_settings import BaseSettings
from pydantic import BaseModel

class ContextConfig(BaseModel):
    mode: str = "semantic"
    compressor: str = "distill"
    budget: int = 6000
    cache: bool = True
    provider: str = "openai"

class ContextSettings(BaseSettings):
    openai_api_key: str = "sk-mock-key"
    max_context_tokens: int = 100000
    default_model: str = "gpt-4o"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Expose a global default singleton for convenience, though dependency injection is preferred.
config = ContextSettings()
