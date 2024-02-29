import json
import logging
import math

from aiogram_dialog import DialogManager

from misc.enums import TypeOfSubject
from models.base import BaseSubject
from utils.caching_handlers import is_exist, get_data, set_data
from utils.tmdb_api import tmdb_search_by_title

async def message_handler(message: Message, message_input: MessageInput, dialog_manager: DialogManager):
    logging.info(f"Message from '{message.from_user.username}' received: '{message.text}'")
    dialog_manager.show_mode = ShowMode.EDIT
    await message.delete()


async def unknown_message_handler(message: Message, *args):
    await message.answer(text=unknown_type_message, parse_mode="HTML")

async def get_list_of_found_movies(dialog_manager: DialogManager, *args, **kwargs) -> dict:
    user_request = dialog_manager.dialog_data["user_request"]
    dialog_manager.dialog_data["current_movie_tmdb_id"] = None

    redis_key = f"keybmovies:{user_request.lower().replace(' ', '')}"

    if await is_exist(redis_key):
        logging.info(f"Retrieving data from Redis by key: {redis_key}")
        cache = await get_data(redis_key)
        keyboard_movies = [BaseSubject(**(json.loads(item)))
                           for item in cache]
    else:
        logging.info(f"Making a API request to TMDB API by title: {user_request}")
        keyboard_movies = await tmdb_search_by_title(user_request, TypeOfSubject.movie)
        cache = [movie.json_data for movie in keyboard_movies]
        await set_data(redis_key, cache)

    number_of_pages = math.ceil(len(keyboard_movies) / 10)
    dialog_manager.dialog_data["total_number_of_keyboard_movies_pages"] = number_of_pages

    keyboard_movies = keyboard_movies[(dialog_manager.dialog_data["current_keyboard_movies_page"] - 1) * 10:
                                      dialog_manager.dialog_data["current_keyboard_movies_page"] * 10]

    next_page_number = dialog_manager.dialog_data["current_keyboard_movies_page"] + 1 if \
        dialog_manager.dialog_data["current_keyboard_movies_page"] + 1 <= number_of_pages \
        else number_of_pages

    prev_page_number = dialog_manager.dialog_data["current_keyboard_movies_page"] - 1 if \
        dialog_manager.dialog_data["current_keyboard_movies_page"] - 1 > 0 \
        else 1

    return {
        "keyboard_movies": keyboard_movies,
        "next_page": keys_emojis[next_page_number],
        "prev_page": keys_emojis[prev_page_number],
    }
