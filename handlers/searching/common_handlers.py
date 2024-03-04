import json
import logging
import math
from typing import List

from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput

from misc.enums import TypeOfSubject, TypeOfSubjectFeature
from models.base import BaseSubject
from utils.caching_handlers import is_exist, get_data, set_data
from utils.tmdb_api import tmdb_search_by_title

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
