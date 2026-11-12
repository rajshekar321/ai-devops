import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "AI-DevOps Control Plane"
    APP_ENV: str = "production"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    DEBUG: bool = False

    # Database configuration with default fallback
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./devops.db"
    )

    # CORS origins
    ALLOWED_ORIGINS: list[str] = ["*"]

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
