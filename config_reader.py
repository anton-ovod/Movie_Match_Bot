from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: SecretStr
    api_key: SecretStr
    base_image_url: SecretStr
    search_movie_url: SecretStr

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


config = Settings()
