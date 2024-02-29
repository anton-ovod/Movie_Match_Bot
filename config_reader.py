from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: SecretStr
    api_key: SecretStr
    base_image_url: SecretStr
    tmdb_search_url: SecretStr
    tmdb_subject_details_url: SecretStr
    base_video_url: SecretStr
    omdb_api_key: SecretStr
    omdb_base_url: SecretStr
    title_imdb_url: SecretStr
    title_tmdb_url: SecretStr
    search_rot_url: SecretStr
    search_meta_url: SecretStr
    youtube_search_url: SecretStr
    person_base_url: SecretStr

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


config = Settings()
