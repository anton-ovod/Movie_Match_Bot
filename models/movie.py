import aiohttp
import logging

from config_reader import config


class Movie:
    def __init__(self, title, release_date, tmdb_id):
        self._title: str = title
        self._year: str = release_date[:4]
        self._tmdb_id: str = tmdb_id

    def __repr__(self):
        return f"{self._title} ({self._year}) : {self._tmdb_id}" if self._year else f"{self._title} : {self._tmdb_id}"

    @property
    def title(self) -> str:
        return f"{self._title} ({self._year})" if self._year else f"{self._title}"

    @property
    def tmdb_id(self) -> str:
        return self._tmdb_id

    @property
    async def get_movie_details(self) -> dict:
        try:
            async with aiohttp.ClientSession() as session:
                movie_details_url = config.movie_details_url.get_secret_value()
                params = {
                    "api_key": config.api_key.get_secret_value(),
                    "language": "en-US",
                    "append_to_response": "credits,videos",
                    "movie_id": f"{self._tmdb_id}"
                }
                async with session.get(movie_details_url, params=params) as response:
                    return await response.json()
        except Exception as e:
            logging.error(f"Error while getting movie details: {e}")
