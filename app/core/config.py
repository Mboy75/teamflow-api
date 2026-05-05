from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
import os



class Settings(BaseSettings):
    #  Environment
    ENV: str = "dev"  # dev | test | prod

    #  App
    PROJECT_NAME: str = "TeamFlow API"
    DEBUG: bool = True

    #  Security
    SECRET_KEY: str = "supersecretkey"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"

    #  Database
    DATABASE_URL: str | None = None

    #  Pydantic v2 config
    model_config = ConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()


def get_database_url():
    #  TEST → SQLite
    if settings.ENV == "test":
        return "sqlite:///./test.db"

    #  Docker / prod
    if settings.DATABASE_URL:
        return settings.DATABASE_URL

    #  fallback locale
    return "sqlite:///./dev.db"