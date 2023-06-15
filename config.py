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

  class Config:
    env_file = '.env'

mongo_settings = MongoSettings()


class JWTSettings:
    algorithm = "HS256"
    secret_key = "mysecretkey"
    access_token_expire = 30
    access_token_expire_minutes = 30
