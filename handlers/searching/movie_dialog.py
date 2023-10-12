import json
import logging
import math
from typing import Any

from aiogram import Router
from aiogram.types import CallbackQuery, Message

from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from misc.states import MovieDialogSG

from utils.caching_handlers import get_data, set_data, is_exist
from utils.tmdb_api import get_movies_by_title

from models.movie import KeyboardMovie

from dialogs.searching import env

movie_search_router = Router()

unknown_type_message = env.get_template("unknown_type_message.jinja2").render()
keys_emojis = {
    1: "1️⃣",
    2: "2️⃣",
    3: "3️⃣",
    4: "4️⃣",
    5: "5️⃣",
    6: "6️⃣",
    7: "7️⃣",
    8: "8️⃣",
    9: "9️⃣",
    10: "🔟",
}


async def init_movie_search_dialog(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    logging.info("Movie search dialog initialized")
    await dialog_manager.start(MovieDialogSG.title_request, show_mode=ShowMode.EDIT)
    await callback.answer("🤖 I'm ready to search for movies!")


async def title_request_handler(message: Message, message_input: MessageInput,
                                dialog_manager: DialogManager):
    dialog_manager.dialog_data["user_request"] = message.text
    logging.info(f"User request: `{message.text}` successfully saved")

    redis_key = f"keybmovies:{message.text.lower().replace(' ', '')}"

    if await is_exist(redis_key):
        logging.info(f"Retrieving data from Redis by key: {redis_key}")
        cache = await get_data(redis_key)
        keyboard_movies = cache
    else:
        logging.info(f"Making a API request to TMDB API by title: {message.text}")
        keyboard_movies = await get_movies_by_title(message.text)
        await set_data(redis_key, keyboard_movies)

    dialog_manager.dialog_data["current_keyboard_movies"] = keyboard_movies
    dialog_manager.dialog_data["current_keyboard_movies_page"] = 1

    logging.info(f"Keyboard movies: {keyboard_movies}")
    await message.delete()
    await dialog_manager.switch_to(MovieDialogSG.movies_pagination, show_mode=ShowMode.EDIT)


async def movie_overview_handler(callback: CallbackQuery, widget: Any,
                                 manager: DialogManager, item_id: str):
    logging.info(f"Movie overview handler: {item_id}")
    await callback.answer("🎬 Movie overview")


async def message_handler(message: Message, message_input: MessageInput, dialog_manager: DialogManager):
    logging.info(f"Message from '{message.from_user.username}' received: '{message.text}'")
    dialog_manager.show_mode = ShowMode.EDIT
    await message.delete()


async def get_list_of_keyboard_movies(dialog_manager: DialogManager, **kwargs):
    keyboard_movies = [KeyboardMovie(**(json.loads(item)))
                       for item in dialog_manager.dialog_data["current_keyboard_movies"]]

    number_of_pages = math.ceil(len(keyboard_movies) / 10)
    dialog_manager.dialog_data["total_number_of_keyboard_movies"] = number_of_pages

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


async def previous_page_handler(callback: CallbackQuery, widget: Any, manager: DialogManager):
    logging.info("Previous page handler")
    if manager.dialog_data["current_keyboard_movies_page"] > 1:
        manager.dialog_data["current_keyboard_movies_page"] -= 1
    await manager.update(data=manager.dialog_data, show_mode=ShowMode.EDIT)
    await callback.answer("Page " + keys_emojis[manager.dialog_data["current_keyboard_movies_page"]])


async def next_page_handler(callback: CallbackQuery, widget: Any, manager: DialogManager):
    logging.info("Next page handler")
    if manager.dialog_data["current_keyboard_movies_page"] < manager.dialog_data["total_number_of_keyboard_movies"]:
        manager.dialog_data["current_keyboard_movies_page"] += 1
    await manager.update(data=manager.dialog_data, show_mode=ShowMode.EDIT)
    await callback.answer("Page " + keys_emojis[manager.dialog_data["current_keyboard_movies_page"]])


async def unknown_message_handler(message: Message, *args):
    await message.answer(text=unknown_type_message, parse_mode="HTML")
