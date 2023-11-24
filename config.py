import os
from pydantic import BaseSettings
from datetime import timedelta


# class Settings(BaseSettings):
#   DATABASE_PORT: int
#   POSTGRES_PASSWORD: str
#   POSTGRES_USER: str
#   POSTGRES_DB: str
#   POSTGRES_HOST: str
#   POSTGRES_HOSTNAME: str

#   class Config:
#     env_file = './.env'

# settings = Settings()


class MongoSettings(BaseSettings):
    MONGO_URI: str
    ADMIN_PASS: str | None = None

    class Config:
        env_file = ".env"


mongo_settings = MongoSettings()


class JWTSettings(BaseSettings):
    algorithm = "HS256"
    SECRET_KEY: str = os.environ.get("SECRET_KEY") or "."
    access_token_expire: int = os.environ.get("TOKEN_EXPIRE") or 30
    access_token_expire_minutes: int = os.environ.get("TOKEN_EXPIRE_MINUTES") or 30

    class Config:
        env_file = ".env"

jwt_settings = JWTSettings()
