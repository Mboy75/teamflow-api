from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):

    ENV: str = "dev" # new variable to determine the environment


    PROJECT_NAME: str = "TeamFlow API"
    DEBUG: bool = True

    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"

    DATABASE_URL: str | None = None
    
    
    #str = Field(
    #    default="sqlite:///./test.db"
    #)

    class Config:
        env_file = ".env"


settings = Settings()


def get_database_url():
    if settings.ENV == "test":
        return "sqlite:///./test.db"

    if settings.DATABASE_URL:
        return settings.DATABASE_URL

    raise ValueError("DATABASE_URL not set")