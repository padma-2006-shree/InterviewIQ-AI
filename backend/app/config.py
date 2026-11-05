import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "InterviewIQ AI"
    version: str = "1.0.0"
    debug: bool = True
    secret_key: str = os.getenv("SECRET_KEY", "interviewiq_default_secret_key_2026")
    openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY", "")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./interviewiq.db")

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
