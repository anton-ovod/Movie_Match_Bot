import aiohttp
import logging

from typing import List

from config_reader import config

from models.movie import KeyboardMovie


async def get_movies_by_title(title: str) -> List[KeyboardMovie]:
    try:
        async with aiohttp.ClientSession() as session:
            search_movie_url = config.search_movie_url.get_secret_value()
            params = {
                "api_key": config.api_key.get_secret_value(),
                "query": title,
                "include_adult": "false",
                "page": "1"
            }
            async with session.get(search_movie_url, params=params) as response:
                data = await response.json()
                results = sorted(data.get("results"), key=lambda x: x.get("popularity"), reverse=True)
                movies = []
                for result in results:
                    movies.append(KeyboardMovie(title=result.get("title"),
                                                release_date=result.get("release_date")
                                                if result.get("release_date") else None,
                                                tmdb_id=result.get("id")))
                return movies
    except Exception as e:
        logging.error(f"Error while getting movies by title: {e}")



