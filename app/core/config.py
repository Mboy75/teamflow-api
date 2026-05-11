from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str = "dev"

    PROJECT_NAME: str = "TeamFlow API"
    DEBUG: bool = True

    SECRET_KEY: str = "supersecretkey"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"

    DATABASE_URL: str | None = None

    model_config = ConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()


def get_database_url() -> str:
    if settings.ENV == "test":
        return settings.DATABASE_URL or "sqlite:///./test.db"

    if settings.ENV == "prod":
        if not settings.DATABASE_URL:
            raise ValueError("DATABASE_URL is required in production")
        return settings.DATABASE_URL

    return settings.DATABASE_URL or "sqlite:///./dev.db"


DATABASE_URL = get_database_url()