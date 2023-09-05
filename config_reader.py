from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: SecretStr
    api_key: SecretStr
    base_image_url: SecretStr
    search_movie_url: SecretStr
    movie_details_url: SecretStr
    base_video_url: SecretStr
    omdb_api_key: SecretStr
    omdb_base_url: SecretStr

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


config = Settings()
