import json
import logging
import math

from aiogram_dialog import DialogManager

from handlers.searching_handlers import ITEMS_PER_PAGE, navigation_emoji
from misc.enums import PaginationLocation, SubjectsModels
from models.base import BaseSubject
from utils.caching_handlers import get_data, is_exist, set_data
from utils.omdb_api import get_subject_details_omdb
from utils.tmdb_api import tmdb_search_by_title, get_subject_details_tmdb, get_subject_suggestions_by_id


async def get_list_of_found_base_subjects_by_title(dialog_manager: DialogManager, *args, **kwargs) -> dict:
    user_request = dialog_manager.dialog_data["user_request"]
    type_of_subject = dialog_manager.dialog_data["subject_type"]

    dialog_manager.dialog_data[f"current_{type_of_subject.lower()}_tmdb_id"] = None
    dialog_manager.dialog_data["pagination_location"] = PaginationLocation.MAIN.value

    redis_key = f"basesubjects:{type_of_subject.lower()}:{user_request.lower().replace(' ', '')}"

    if await is_exist(redis_key):
        logging.info(f"Retrieving data from Redis by key: {redis_key}")
        cache = await get_data(redis_key)
        subject_class = getattr(SubjectsModels, type_of_subject).base_class
        base_subjects = [subject_class(**(json.loads(item)))
                         for item in cache]
    else:
        logging.info(f"Making a API request by title: {user_request}")
        base_subjects = await tmdb_search_by_title(user_request, type_of_subject.lower())
        if base_subjects:
            cache = [item.json_data for item in base_subjects]
            await set_data(redis_key, cache)

    current_base_subjects_page = dialog_manager.dialog_data["main_pagination_current_page"]

    total_number_of_pages = math.ceil(len(base_subjects) / ITEMS_PER_PAGE)
    dialog_manager.dialog_data["total_main_pagination_pages"] = total_number_of_pages

    next_page_number = current_base_subjects_page + 1 if (current_base_subjects_page + 1
                                                          <= total_number_of_pages) else total_number_of_pages

    prev_page_number = current_base_subjects_page - 1 if current_base_subjects_page - 1 > 0 else 1

    return {
        "base_subjects": base_subjects[(current_base_subjects_page - 1) * ITEMS_PER_PAGE:
                                       current_base_subjects_page * ITEMS_PER_PAGE],
        "next_page": navigation_emoji.format(number_of_page=next_page_number).encode('utf-8').decode('unicode-escape'),
        "prev_page": navigation_emoji.format(number_of_page=prev_page_number).encode('utf-8').decode('unicode-escape'),
        "current_page": current_base_subjects_page,
        "total_number_of_pages": total_number_of_pages
    }


async def get_subject_overview_by_id(dialog_manager: DialogManager, *args, **kwargs) -> dict:
    type_of_subject = dialog_manager.dialog_data["subject_type"]
    subject_tmdb_id = dialog_manager.dialog_data[f"current_{type_of_subject.lower()}_tmdb_id"]

    redis_key = f"{type_of_subject.lower()}:overview:{subject_tmdb_id}"

    subject_class = getattr(SubjectsModels, type_of_subject).detailed_class

    if await is_exist(redis_key):
        logging.info(f"Retrieving data from Redis by key: {redis_key}")
        cache = await get_data(redis_key)
        subject = subject_class(**(json.loads(cache)))
    else:
        logging.info(f"Making a API request to TMDB API by {type_of_subject.lower()} id: {subject_tmdb_id}")
        subject = subject_class(tmdb_id=subject_tmdb_id)
        await get_subject_details_tmdb(subject, type_of_subject.lower())
        if subject.imdb_id:
            await get_subject_details_omdb(subject)
        logging.info(f"{type_of_subject.lower()} overview details: " + subject.json_data)
        await set_data(redis_key, subject.json_data)

    dialog_manager.dialog_data["current_movie_pretty_title"] = subject.pretty_title
    return subject.model_dump()


async def get_list_of_subject_suggestions_by_id(dialog_manager: DialogManager, *args, **kwargs) -> dict:
    type_of_subject = dialog_manager.dialog_data["subject_type"]
    subject_tmdb_id = dialog_manager.dialog_data[f"current_{type_of_subject.lower()}_tmdb_id"]

    redis_key = f"basesubjects:{type_of_subject.lower()}:suggestions:{subject_tmdb_id}"

    if await is_exist(redis_key):
        logging.info(f"[{type_of_subject.lower()} suggestions] Retrieving data from Redis by key: {redis_key}")
        cache = await get_data(redis_key)
        subject_class = getattr(SubjectsModels, type_of_subject).base_class
        subject_suggestions = [subject_class(**(json.loads(item))) for item in cache]
    else:
        logging.info(
            f"[{type_of_subject.lower()} suggestions] Making a API request to TMDB API by id: {subject_tmdb_id}")
        subject_suggestions = await get_subject_suggestions_by_id(subject_tmdb_id, type_of_subject.lower())
        if subject_suggestions:
            cache = [item.json_data for item in subject_suggestions]
            await set_data(redis_key, cache)

    current_subject_suggestions_page = dialog_manager.dialog_data["suggestions_pagination_current_page"]

    total_number_of_pages = math.ceil(len(subject_suggestions) / ITEMS_PER_PAGE)

    dialog_manager.dialog_data["total_suggestions_pagination_pages"] = total_number_of_pages

    next_page_number = current_subject_suggestions_page + 1 if (current_subject_suggestions_page + 1
                                                                <= total_number_of_pages) else total_number_of_pages

    prev_page_number = current_subject_suggestions_page - 1 if current_subject_suggestions_page - 1 > 0 else 1

    return {
        "base_subjects": subject_suggestions[(current_subject_suggestions_page - 1) * ITEMS_PER_PAGE:
                                             current_subject_suggestions_page * ITEMS_PER_PAGE],
        "next_page": navigation_emoji.format(number_of_page=next_page_number).encode('utf-8').decode('unicode-escape'),
        "prev_page": navigation_emoji.format(number_of_page=prev_page_number).encode('utf-8').decode('unicode-escape'),
        "current_page": current_subject_suggestions_page,
        "total_number_of_pages": total_number_of_pages
    }
