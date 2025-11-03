from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    testing: bool = False
    redis_url: str = "redis://localhost"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()