import json
import logging
import math
from typing import List

from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput

from misc.enums import TypeOfSubject, PaginationDirection
from models.base import BaseSubject
from models.movie import Movie
from models.tvshow import TVShow
from models.person import Person
from utils.caching_handlers import is_exist, get_data, set_data
from utils.omdb_api import get_subject_details_omdb
from utils.tmdb_api import tmdb_search_by_title, get_subject_details_tmdb

from dialogs.searching import env

unknown_type_message = env.get_template("common/unknown_type_message.jinja2").render()


async def message_handler(message: Message, message_input: MessageInput, dialog_manager: DialogManager):
    logging.info(f"Message from '{message.from_user.username}' received: '{message.text}'")
    dialog_manager.show_mode = ShowMode.EDIT
    await message.delete()


async def unknown_message_handler(message: Message, *args):
    await message.answer(text=unknown_type_message, parse_mode="HTML")


async def subject_title_request_handler(message: Message,
                                        dialog_manager: DialogManager,
                                        type_of_subject: TypeOfSubject):
    if not message.html_text.isascii():
        await unknown_message_handler(message)
    else:
        dialog_manager.dialog_data["user_request"] = message.text
        logging.info(f"[{type_of_subject.value} Search] User request: `{message.text}` successfully saved")

        dialog_manager.dialog_data[f"current_base_{type_of_subject.value}s_page"] = 1
        if "suggestions_depth_stack" not in dialog_manager.dialog_data:
            dialog_manager.dialog_data["suggestions_depth_stack"] = []


async def get_list_of_found_base_subjects_by_title(user_request: str,
                                                   type_of_subject: TypeOfSubject,
                                                   *args, **kwargs) -> List[BaseSubject]:
    redis_key = f"basesubjects:{type_of_subject.value}:{user_request.lower().replace(' ', '')}"

    if await is_exist(redis_key):
        logging.info(f"Retrieving data from Redis by key: {redis_key}")
        cache = await get_data(redis_key)
        base_subjects = [BaseSubject(**(json.loads(item)))
                         for item in cache]
    else:
        logging.info(f"Making a API request by title: {user_request}")
        base_subjects = await tmdb_search_by_title(user_request, TypeOfSubject.movie)
        cache = [item.json_data for item in base_subjects]
        await set_data(redis_key, cache)

    return base_subjects


async def get_subject_overview_by_id(subject_id: int,
                                     type_of_subject: TypeOfSubject) -> Movie | TVShow | Person:

    redis_key = f"{type_of_subject.value}:overview:{subject_id}"
    # create a dict that will write to a specific type of subject specific class name

    class_name = {
        TypeOfSubject.movie: Movie,
        TypeOfSubject.tv_show: TVShow,
        TypeOfSubject.person: Person
    }

    subject_class = class_name[type_of_subject]

    if await is_exist(redis_key):
        logging.info(f"Retrieving data from Redis by key: {redis_key}")
        cache = await get_data(redis_key)
        subject = subject_class(**(json.loads(cache)))
    else:
        logging.info(f"Making a API request to TMDB API by {type_of_subject.value} id: {subject_id}")
        subject = subject_class(tmdb_id=subject_id)
        await get_subject_details_tmdb(subject, type_of_subject)
        if subject.imdb_id:
            await get_subject_details_omdb(subject)
        logging.info(f"{type_of_subject.value} overview details: " + subject.json_data)
        await set_data(redis_key, subject.json_data)

    return subject

async def calculate_pagination(base_subjects: List[BaseSubject], dialog_manager: DialogManager,
                               items_per_page: int, type_of_subject: TypeOfSubject) -> (int, int):
    number_of_pages = math.ceil(len(base_subjects) / items_per_page)
    dialog_manager.dialog_data[f"total_number_of_base_{type_of_subject.value}s_pages"] = number_of_pages

    next_page_number = dialog_manager.dialog_data[f"current_base_{type_of_subject.value}s_page"] + 1 if \
        dialog_manager.dialog_data[f"current_base_{type_of_subject.value}s_page"] + 1 <= number_of_pages \
        else number_of_pages

    prev_page_number = dialog_manager.dialog_data[f"current_base_{type_of_subject.value}s_page"] - 1 if \
        dialog_manager.dialog_data[f"current_base_{type_of_subject.value}s_page"] - 1 > 0 \
        else 1

    return next_page_number, prev_page_number


async def pagination_handler(dialog_manager: DialogManager, direction: PaginationDirection,
                             type_of_subject: TypeOfSubject):
    total_number_of_pages = dialog_manager.dialog_data[f"total_number_of_base_{type_of_subject.value}s_pages"]
    current_page = dialog_manager.dialog_data[f"current_base_{type_of_subject.value}s_page"]

    current_page += direction.value

    if current_page < 1:
        current_page = 1
    elif current_page > total_number_of_pages:
        current_page = total_number_of_pages

    dialog_manager.dialog_data[f"current_base_{type_of_subject.value}s_page"] = current_page
