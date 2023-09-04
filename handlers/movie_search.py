import aiohttp
import logging

from typing import List

from config_reader import config

from models.movie import Movie


async def get_movies_by_title(title: str) -> dict:
    try:
        async with aiohttp.ClientSession() as session:
            search_movie_url = config.search_movie_url.get_secret_value()
            params = {
                "api_key": config.api_key.get_secret_value(),
                "query": title,
                "include_adult": "true",
                "page": "1"
            }
            async with session.get(search_movie_url, params=params) as response:
                return await response.json()
    except Exception as e:
        logging.error(f"Error while getting movies by title: {e}")


async def get_list_of_movies_for_keyboard(title: str) -> (List[Movie], int):
    movies_data = await get_movies_by_title(title)
    movies = []
    movies_number = len(movies_data.get("results", []))
    for movie in movies_data.get("results", []):
        movies.append(Movie(movie.get("title", "Unknown title"), movie.get("release_date", "Unknown release date"),
                            str(movie.get("id", "Unknown id"))))
    return movies, movies_number
