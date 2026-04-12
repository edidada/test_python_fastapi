from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    APP_NAME: str = "Blog FastAPI"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    
    SECRET_KEY: str = "dev-secret-key-change-in-production-please"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    
    DATABASE_URL: str = "sqlite:///./blog.db"
    
    class Config:
        env_file = str(BASE_DIR / ".env")


@lru_cache()
def get_settings():
    return Settings()
