import aiohttp
import logging

from config_reader import config

from models.movie import Movie, Rating


async def get_movie_details_omdb(movie: Movie) -> None:
    try:
        async with aiohttp.ClientSession() as session:
            movie_details_url = config.omdb_base_url.get_secret_value()
            params = {
                "apikey": config.omdb_api_key.get_secret_value(),
                "i": movie.imdb_id,
            }
            async with session.get(movie_details_url, params=params) as response:
                movie_detail = await response.json()
                if countries := movie_detail.get("Country"):
                    movie.countries = countries.split(", ")
                if age_categories := movie_detail.get("Rated"):
                    if age_categories != "N/A":
                        movie.age_categories = age_categories
                if awards := movie_detail.get("Awards"):
                    if awards != "N/A":
                        movie.awards = awards
                if ratings := movie_detail.get("Ratings"):
                    for rating in ratings[1:]:
                        movie.ratings.append(Rating(source=rating.get("Source"), value=int(rating.get("Value")[0:2])))
                if imdb_rating := movie_detail.get("imdbRating"):
                    movie.ratings.append(Rating(source="IMDB", value=float(imdb_rating)))
    except Exception as e:
        logging.error(f"Error while getting movie details(OMDB): {e}")
