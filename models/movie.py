import asyncio

import aiohttp
import logging

from typing import Dict, List

from config_reader import config


class KeyboardMovie:
    def __init__(self, title, release_date, tmdb_id):
        self._title: str = title
        self._year: str = release_date[:4]
        self._tmdb_id: str = tmdb_id

    def __repr__(self):
        return f"Keyboard Movie: {self.title} : {self._tmdb_id}"

    @property
    def title(self) -> str:
        return f"{self._title} ({self._year})" if self._year else f"{self._title}"

    @property
    def get_main_data(self) -> Dict[str, str]:
        return {
            "title": self._title,
            "release_date": self._year,
            "tmdb_id":  self._tmdb_id
        }


class Movie:
    def __init__(self, tmdb_id):
        self._tmdb_id: int = tmdb_id
        self.imdb_id: str = ""
        self.title: str = ""
        self.release_date: str = ""
        self.overview: str = ""
        self.tagline: str = ""
        self.genres: List[str] = []
        self.runtime: str = ""
        self.ratings: List[Dict[str, str]] = []
        self.poster_url: str = "https://dummyimage.com/300x400/cccccc/ffffff&text=Poster+Not+Found"  # Poster not found
        self.trailer_url: str = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Roll
        self.cast: List[Dict[str, str]] = []
        self.homepage: str = ""
        self.awards: str = ""
        self.year_categories: List[str] = []

    async def get_movie_details_tmdb(self):
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
                    logging.info(movie_detail)
                    self.title = movie_detail.get("title", "Unknown title")
                    self.release_date = movie_detail.get("release_date", "Unknown release date")
                    self.tagline = movie_detail.get("tagline", "Unknown tagline")
                    self.genres = [genre.get("name", "") for genre in movie_detail.get("genres", [])]
                    self.homepage = movie_detail.get("homepage", "")
                    self.overview = movie_detail.get("overview", "Unknown overview")
                    self.imdb_id = str(movie_detail.get("imdb_id", "Unknown imdb id"))
                    self.runtime = str(movie_detail.get("runtime", "Unknown runtime"))

                    if movie_detail.get("poster_path", ""):
                        self.poster_url = f"{config.base_image_url.get_secret_value()}{movie_detail.get('poster_path')}"

                    if movie_detail.get("videos", {}).get("results", []):
                        for video in movie_detail.get("videos", {}).get("results", []):
                            if video.get("type", "") == "Trailer":
                                self.trailer_url = f"{config.base_video_url}{video.get('key')}"
                                break

                    if movie_detail.get("credits", {}).get("cast", []):
                        for cast in movie_detail.get("credits", {}).get("cast", [])[:3]:
                            self.cast.append({
                                "name": cast.get("name", "Unknown name"),
                                "character": cast.get("character", "Unknown character"),
                                "profile_path": f"{config.base_image_url.get_secret_value()}{cast.get('profile_path')}"
                            })
        except Exception as e:
            logging.error(f"Error while getting movie details(TMDB): {e}")

    async def get_movie_details_omdb(self):
        try:
            async with aiohttp.ClientSession() as session:
                movie_details_url = config.omdb_base_url.get_secret_value()
                logging.info("IMDB ID: " + self.imdb_id)
                params = {
                    "apikey": config.omdb_api_key.get_secret_value(),
                    "i": self.imdb_id,
                    "plot": "full"
                }
                async with session.get(movie_details_url, params=params) as response:
                    movie_detail = await response.json()
                    logging.info(movie_detail)
                    self.awards = movie_detail.get("Awards", "No Awards")
                    if movie_detail.get("Ratings", []):
                        for rating in movie_detail.get("Ratings", []):
                            self.ratings.append({
                                "source": rating.get("Source", ""),
                                "value": rating.get("Value", "")
                            })
                    self.ratings.append({
                        "source": "Metascore",
                        "value": movie_detail.get("Metascore", "")
                    })
        except Exception as e:
            logging.error(f"Error while getting movie details(OMDB): {e}")

    async def get_movie_details(self):
        await self.get_movie_details_tmdb()
        await self.get_movie_details_omdb()


