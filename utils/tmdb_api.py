import json

import aiohttp
import logging

from typing import List, Dict
from config_reader import config
from datetime import datetime

from models.movie import KeyboardMovie, Movie, Actor, Rating, Provider
from models.tvshow import TVShow
from models.person import Person

from misc.enums import TypeOfSubject


def create_list_of_keyboard_movies(data: List[Dict]) -> List[KeyboardMovie]:
    results = []
    for item in data:
        title = item.get("title")
        tmdb_id = item.get("id")
        try:
            release_date = datetime.strptime(item.get("release_date"), "%Y-%m-%d").date() or \
                           datetime.strptime(item.get("first_air_date"), "%Y-%m-%d").date()
        except ValueError:
            release_date = None
        pretty_title = f"{title} ({release_date.year})" if release_date else title
        results.append(KeyboardMovie(title=title,
                                     pretty_title=pretty_title,
                                     release_date=release_date,
                                     tmdb_id=tmdb_id))
    return results


# Functions to get data from TMDb API for movies
async def tmdb_search_by_title(title: str, type_of_subject: TypeOfSubject) -> list[KeyboardMovie]:
    try:
        async with aiohttp.ClientSession() as session:
            search_subject_url = config.tmdb_search_url.get_secret_value() + type_of_subject.value
            params = {
                "api_key": config.api_key.get_secret_value(),
                "query": title,
                "include_adult": "false",
                "page": "1"
            }
            async with session.get(search_subject_url, params=params) as response:
                data = await response.json()
                sorted_data = sorted(data.get("results"), key=lambda x: x.get("popularity"), reverse=True)

                results = create_list_of_keyboard_movies(sorted_data)

                return results
    except Exception as e:
        logging.error(f"[TMDB API] Error while searching by title: {e}")


async def get_subject_details_tmdb(subject: Movie | TVShow | Person, type_of_subject: TypeOfSubject) -> None:
    try:
        async with (aiohttp.ClientSession() as session):
            subject_details_url = (f"{config.tmdb_subject_details_url.get_secret_value()}/"
                                   f"{type_of_subject.value}/{subject.tmdb_id}")
            params = {
                "api_key": config.api_key.get_secret_value(),
                "language": "en-US",
                "append_to_response": "credits,videos,watch/providers",
            }
            async with session.get(subject_details_url, params=params) as response:
                movie_detail = await response.json()  # raw data from tmdb api

                # getting basic movie details
                if title := movie_detail.get("title"):
                    subject.title = title
                if release_date := movie_detail.get("release_date"):
                    subject.release_date = datetime.strptime(release_date, "%Y-%m-%d").date()

                subject.pretty_title = f"{subject.title} ({subject.release_date.year})" \
                    if subject.release_date else subject.title

                if imdb_id := movie_detail.get("imdb_id"):
                    subject.imdb_id = imdb_id
                if tagline := movie_detail.get("tagline"):
                    subject.tagline = tagline
                if overview := movie_detail.get("overview"):
                    subject.overview = overview
                if poster_path := movie_detail.get("poster_path"):
                    subject.poster_url = f'{config.base_image_url.get_secret_value()}{poster_path}'
                if genres := movie_detail.get("genres"):
                    subject.genres = [genre.get("name") for genre in genres]
                if runtime := movie_detail.get("runtime"):
                    subject.runtime = runtime
                if homepage := movie_detail.get("homepage"):
                    subject.homepage = homepage
                if tmdb_rating := movie_detail.get("vote_average"):
                    subject.ratings.append(Rating(source="TMDb", value=int(tmdb_rating) * 10))

                # getting key for YouTube trailer and creating a link
                if videos := movie_detail.get("videos").get("results"):
                    for video in videos:
                        if video.get("type") == "Trailer":
                            subject.trailer_url = f'{config.base_video_url.get_secret_value()}{video.get("key")}'
                            break
                    else:
                        subject.trailer_url = (f'{config.youtube_search_url.get_secret_value()}trailer+'
                                               f'{subject.title.replace(" ", "+")}')
                else:
                    subject.trailer_url = (f'{config.youtube_search_url.get_secret_value()}trailer+'
                                           f'{subject.title.replace(" ", "+")}')

                # getting cast details and creating links for actors
                if actors := movie_detail.get("credits").get("cast"):
                    for actor in actors[:3]:
                        subject.cast.append(Actor(name=actor.get("name"),
                                                  character=actor.get("character"),
                                                  profile_url=f'{config.person_base_url.get_secret_value()}'
                                                              f'{actor.get("id")}'))
                # getting crew details and creating links for actors
                if crew := movie_detail.get("credits").get("crew"):
                    for crew_member in crew:
                        if crew_member.get("job") == "Director":
                            subject.cast.append(Actor(name=crew_member.get("name"),
                                                      character="Director",
                                                      profile_url=f'{config.person_base_url.get_secret_value()}'
                                                                  f'{crew_member.get("id")}'))
                            break

                # getting providers details and deep link for movie
                if providers := movie_detail.get("watch/providers").get("results"):
                    if us := providers.get("US"):
                        subject.providers_deep_link = us.get("link")
                        if flatrate := us.get("flatrate"):
                            for provider in flatrate:
                                subject.providers["flatrate"].append(
                                    Provider(provider_name=provider.get("provider_name"),
                                             provider_logo_url=f'{config.base_image_url.get_secret_value()}'
                                                               f'{provider.get("logo_path")}'))
                        if rent := us.get("rent"):
                            for provider in rent:
                                subject.providers["rent"].append(
                                    Provider(provider_name=provider.get("provider_name"),
                                             provider_logo_url=f'{config.base_image_url.get_secret_value()}'
                                                               f'{provider.get("logo_path")}'))
                        if buy := us.get("buy"):
                            for provider in buy:
                                subject.providers["buy"].append(
                                    Provider(provider_name=provider.get("provider_name"),
                                             provider_logo_url=f'{config.base_image_url.get_secret_value()}'
                                                               f'{provider.get("logo_path")}'))
    except Exception as e:
        logging.error(f"Error while getting movie details(TMDB): {e}")


async def get_suggestions_by_id(tmdb_id: int, type_of_subject: TypeOfSubject) -> List[KeyboardMovie]:
    try:
        async with aiohttp.ClientSession() as session:
            subject_recommendations_url = (f"{config.tmdb_subject_details_url.get_secret_value()}/"
                                           f"{type_of_subject.value}/{tmdb_id}/similar")
            params = {
                "api_key": config.api_key.get_secret_value(),
                "language": "en-US",
                "page": "1"
            }
            async with session.get(subject_recommendations_url, params=params) as response:
                data = await response.json()
                sorted_data = sorted(data.get("results"), key=lambda x: x.get("popularity"), reverse=True)

                recommendations = create_list_of_keyboard_movies(sorted_data)

                return recommendations
    except Exception as e:
        logging.error(f"[TMDB API] Error while getting recommendations by id: {e}")

# Functions to get different data from TMDb API for tv shows
# async def get_tvshows_by_title(title: str) -> list[KeyboardMovie]:
