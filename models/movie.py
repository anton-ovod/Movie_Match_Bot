import aiohttp
import logging

from pydantic import BaseModel, PositiveInt
from datetime import date

from config_reader import config


class KeyboardMovie(BaseModel):
    title: str
    release_date: date | None
    tmdb_id: PositiveInt

    @property
    def pretty_title(self) -> str:
        return self.title + f" ({self.release_date.year})" if self.release_date else self.title


class Movie(KeyboardMovie):

    async def _get_movie_details_tmdb(self) -> None:
        try:
            async with aiohttp.ClientSession() as session:
                movie_details_url = f"{config.movie_details_url.get_secret_value()}/{self._tmdb_id}"
                params = {
                    "api_key": config.api_key.get_secret_value(),
                    "language": "en-US",
                    "append_to_response": "credits,videos",
                }
                async with session.get(movie_details_url, params=params) as response:
                    movie_detail = await response.json()
        except Exception as e:
            logging.error(f"Error while getting movie details(TMDB): {e}")

    async def _get_movie_details_omdb(self) -> None:
        try:
            async with aiohttp.ClientSession() as session:
                movie_details_url = config.omdb_base_url.get_secret_value()
                logging.info("IMDB ID: " + self._imdb_id)
                params = {
                    "apikey": config.omdb_api_key.get_secret_value(),
                    "i": self._imdb_id,
                }
                async with session.get(movie_details_url, params=params) as response:
                    movie_detail = await response.json()
        except Exception as e:
            logging.error(f"Error while getting movie details(OMDB): {e}")

    def _create_html_movie_ratings(self) -> str:
        star_characters = {
            0: "🌑🌑🌑🌑🌑",
            0.5: "🌗🌑🌑🌑🌑",
            1: "🌕🌑🌑🌑🌑",
            1.5: "🌕🌗🌑🌑🌑",
            2: "🌕🌕🌑🌑🌑",
            2.5: "🌕🌕🌗🌑🌑",
            3: "🌕🌕🌕🌑🌑",
            3.5: "🌕🌕🌕🌗🌑",
            4: "🌕🌕🌕🌕🌑",
            4.5: "🌕🌕🌕🌕🌗",
            5: "🌕🌕🌕🌕🌕"
        }
        average_rating = self._calculate_average_rating()
        try:
            star_rating = star_characters[round((average_rating / 20) * 2) / 2]
        except (TypeError, KeyError):
            star_rating = star_characters[0]

        return ""
