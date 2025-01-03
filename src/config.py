import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    DB_URL: str
    OPENAI_API_KEY: str

    # OAuth2
    OAUTH2_SECRET_KEY: str = "mysecretkey"
    OAUTH2_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Redis (캐시) 예시
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    class Config:
        env_file = ".env"

settings = Settings()
