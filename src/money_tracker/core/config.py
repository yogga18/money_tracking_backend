from pydantic_settings import BaseSettings
from functools import lru_cache
from pydantic import computed_field

class Settings(BaseSettings):
    # App
    APP_NAME: str = "Money Tracker API"
    DEBUG: bool = False
    
    # Database (Postgres)
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    # Google Auth
    GOOGLE_CLIENT_ID: str

    # JWT Security
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    # Redis
    # REDIS_URL: str = "redis://localhost:6379/0" # Default fallback
    
    # Qdrant
    # QDRANT_URL: str = self.QDRANT_URL
    # QDRANT_API_KEY: str | None = None

    class Config:
        env_file = (".env", "../.env")
        extra = "ignore" # Ignore extra fields in .env

@lru_cache
def get_settings():
    return Settings()
