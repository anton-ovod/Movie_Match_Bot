import aiohttp
import logging

from typing import List
from config_reader import config

from models.movie import KeyboardMovie, Movie, Actor, Rating


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


async def get_movie_details_tmdb(movie: Movie) -> None:
    try:
        async with aiohttp.ClientSession() as session:
            movie_details_url = f"{config.movie_details_url.get_secret_value()}/{movie.tmdb_id}"
            params = {
                "api_key": config.api_key.get_secret_value(),
                "language": "en-US",
                "append_to_response": "credits,videos",
            }
            async with session.get(movie_details_url, params=params) as response:
                movie_detail = await response.json()
                if imdb_id := movie_detail.get("imdb_id"):
                    movie.imdb_id = imdb_id
                if tagline := movie_detail.get("tagline"):
                    movie.tagline = tagline
                if overview := movie_detail.get("overview"):
                    movie.overview = overview
                if poster_path := movie_detail.get("poster_path"):
                    movie.poster_url = f'{config.base_image_url.get_secret_value()}{poster_path}'
                if videos := movie_detail.get("videos").get("results"):
                    for video in videos:
                        if video.get("type") == "Trailer":
                            movie.trailer_url = f'{config.base_video_url.get_secret_value()}{video.get("key")}'
                            break
                else:
                    movie.trailer_url = f'{config.youtube_search_url.get_secret_value()}trailer {movie.pretty_title}'
                if genres := movie_detail.get("genres"):
                    movie.genres = [genre.get("name") for genre in genres]
                if runtime := movie_detail.get("runtime"):
                    movie.runtime = runtime
                if actors := movie_detail.get("credits").get("cast"):
                    for actor in actors[:3]:
                        movie.cast.append(Actor(name=actor.get("name"),
                                                character=actor.get("character"),
                                                profile_url=f'{config.person_base_url.get_secret_value()}'
                                                            f'{actor.get("id")}'))
                if homepage := movie_detail.get("homepage"):
                    movie.homepage = homepage
                if tmdb_rating := movie_detail.get("vote_average"):
                    movie.ratings.append(Rating(source="TMDb", value=int(tmdb_rating) * 10))
                else:
                    movie.ratings.append(Rating(source="TMDb", value=0))

    except Exception as e:
        logging.error(f"Error while getting movie details(TMDB): {e}")
