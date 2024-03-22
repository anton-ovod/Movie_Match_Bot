import aiohttp
import logging

from typing import List, Dict
from config_reader import config
from datetime import datetime

from misc.enums import SubjectsModels

from models.base import BaseSubject, BaseMovie, BaseTVShow, BasePerson
from models.common import Rating, Actor, Provider
from models.detailedmovie import DetailedMovie
from models.detailedtvshow import DetailedTVShow
from models.detailedperson import DetailedPerson


def create_list_of_base_subjects(data: List[Dict], type_of_subject: str) -> List[BaseMovie | BaseTVShow | BasePerson]:
    results = []
    attributes = {}
    for item in data:
        if title := item.get("title"):
            attributes["title"] = title

        if name := item.get("name"):
            attributes["name"] = name

        attributes["tmdb_id"] = item.get("id")

        if 'release_date' in item:
            try:
                str_date = item.get("release_date")
                release_date = datetime.strptime(str_date, "%Y-%m-%d").date()
            except (ValueError, TypeError):
                release_date = None
            attributes["release_date"] = release_date

        if 'first_air_date' in item:
            try:
                str_date = item.get("first_air_date")
                first_air_date = datetime.strptime(str_date, "%Y-%m-%d").date()
            except (ValueError, TypeError):
                first_air_date = None
            attributes["first_air_date"] = first_air_date

        if known_for_department := item.get("known_for_department"):
            attributes["known_for_department"] = known_for_department
            pretty_title = f"{title} ({known_for_department})"
            attributes["pretty_title"] = pretty_title

        if release_date := attributes.get("release_date"):
            pretty_title = f"{title} ({release_date.year})"
            attributes["pretty_title"] = pretty_title

        elif first_air_date := attributes.get("first_air_date"):
            pretty_title = f"{name} ({first_air_date.year})"
            attributes["pretty_title"] = pretty_title

        try:
            subject_class = getattr(SubjectsModels, type_of_subject).base_class
        except ValueError as e:
            logging.error(f"[TMDB API] Error while creating list of base subjects: {e}")
            return []

        results.append(subject_class(**attributes))
    return results


# Functions to get data from TMDb API for movies
async def tmdb_search_by_title(title: str, type_of_subject: str) -> List[BaseSubject]:
    try:
        async with aiohttp.ClientSession() as session:
            search_subject_url = config.tmdb_search_url.get_secret_value() + type_of_subject
            params = {
                "api_key": config.api_key.get_secret_value(),
                "query": title,
                "include_adult": "false",
                "page": "1"
            }
            async with session.get(search_subject_url, params=params) as response:
                data = await response.json()
                sorted_data = sorted(data.get("results"), key=lambda x: x.get("popularity"), reverse=True)

                results = create_list_of_base_subjects(sorted_data, type_of_subject)

                return results
    except Exception as e:
        logging.error(f"[TMDB API] Error while searching by title: {e}")


async def get_subject_details_tmdb(subject: DetailedMovie | DetailedTVShow | DetailedPerson,
                                   type_of_subject: str) -> None:
    try:
        async with (aiohttp.ClientSession() as session):
            subject_details_url = (f"{config.tmdb_subject_details_url.get_secret_value()}/"
                                   f"{type_of_subject}/{subject.tmdb_id}")
            params = {
                "api_key": config.api_key.get_secret_value(),
                "language": "en-US",
                "append_to_response": "credits,videos,watch/providers,external_ids",
            }
            async with session.get(subject_details_url, params=params) as response:
                subject_json_data = await response.json()

                # getting basic subject details
                if title := subject_json_data.get("title"):
                    subject.title = title
                if release_date := subject_json_data.get("release_date"):
                    subject.release_date = datetime.strptime(release_date, "%Y-%m-%d").date()

                subject.pretty_title = f"{subject.title} ({subject.release_date.year})" \
                    if subject.release_date else subject.title

                if imdb_id := subject_json_data.get("imdb_id"):
                    subject.imdb_id = imdb_id
                if tagline := subject_json_data.get("tagline"):
                    subject.tagline = tagline
                if overview := subject_json_data.get("overview"):
                    subject.overview = overview
                if poster_path := subject_json_data.get("poster_path"):
                    subject.poster_url = f'{config.base_image_url.get_secret_value()}{poster_path}'
                if genres := subject_json_data.get("genres"):
                    subject.genres = [genre.get("name") for genre in genres]
                if runtime := subject_json_data.get("runtime"):
                    subject.runtime = runtime
                if homepage := subject_json_data.get("homepage"):
                    subject.homepage = homepage
                if tmdb_rating := subject_json_data.get("vote_average"):
                    subject.ratings.append(Rating(source="TMDb", value=int(tmdb_rating) * 10))

                # getting key for YouTube trailer and creating a link
                if videos := subject_json_data.get("videos").get("results"):
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
                if actors := subject_json_data.get("credits").get("cast"):
                    for actor in actors[:3]:
                        subject.cast.append(Actor(name=actor.get("name"),
                                                  character=actor.get("character"),
                                                  profile_url=f'{config.person_base_url.get_secret_value()}'
                                                              f'{actor.get("id")}'))
                # getting crew details and creating links for director
                if crew := subject_json_data.get("credits").get("crew"):
                    for crew_member in crew:
                        if crew_member.get("job") == "Director":
                            subject.cast.append(Actor(name=crew_member.get("name"),
                                                      character="Director",
                                                      profile_url=f'{config.person_base_url.get_secret_value()}'
                                                                  f'{crew_member.get("id")}'))
                            break

                # getting providers details and deep link
                if providers := subject_json_data.get("watch/providers").get("results"):
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
        logging.error(f"[TMDB API] Error while getting subject's details: {e}")


async def get_subject_suggestions_by_id(tmdb_id: int, type_of_subject: str) -> List[BaseSubject]:
    try:
        async with aiohttp.ClientSession() as session:
            subject_recommendations_url = (f"{config.tmdb_subject_details_url.get_secret_value()}/"
                                           f"{type_of_subject}/{tmdb_id}/similar")
            params = {
                "api_key": config.api_key.get_secret_value(),
                "language": "en-US",
                "page": "1"
            }
            async with session.get(subject_recommendations_url, params=params) as response:
                data = await response.json()
                sorted_data = sorted(data.get("results"), key=lambda x: x.get("popularity"), reverse=True)

                recommendations = create_list_of_base_subjects(sorted_data)

                return recommendations
    except Exception as e:
        logging.error(f"[TMDB API] Error while getting suggestions by id: {e}")
