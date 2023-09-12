import aiohttp
import logging

from config_reader import config

from models.movie import Movie


async def get_movie_details_omdb(movie: Movie) -> None:
    try:
        async with aiohttp.ClientSession() as session:
            movie_details_url = config.omdb_base_url.get_secret_value()
            logging.info("IMDB ID: " + movie.imdb_id)
            params = {
                "apikey": config.omdb_api_key.get_secret_value(),
                "i": movie.imdb_id,
            }
            async with session.get(movie_details_url, params=params) as response:
                movie_detail = await response.json()

    except Exception as e:
        logging.error(f"Error while getting movie details(OMDB): {e}")
