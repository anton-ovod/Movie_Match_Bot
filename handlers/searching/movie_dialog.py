import json
import logging
import math

from aiogram import Router
from aiogram.types import CallbackQuery, Message

from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from misc.states import MovieDialogSG

from utils.caching_handlers import get_data, set_data, is_exist
from utils.tmdb_api import (get_movies_by_title, get_movie_details_tmdb, get_suggestions_by_id)

from utils.omdb_api import get_movie_details_omdb

from models.movie import KeyboardMovie, Movie

from dialogs.searching import env

movie_search_router = Router()

unknown_type_message = env.get_template("common/unknown_type_message.jinja2").render()
no_results_message = env.get_template("movie/no_results_message.jinja2").render()
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
    if not message.html_text.isascii():
        await message.answer(text=unknown_type_message, parse_mode="HTML")

    else:
        dialog_manager.dialog_data["user_request"] = message.text
        logging.info(f"[Movie Search] User request: `{message.text}` successfully saved")

        dialog_manager.dialog_data["current_keyboard_movies_page"] = 1
        if "suggestions_depth_stack" not in dialog_manager.dialog_data:
            dialog_manager.dialog_data["suggestions_depth_stack"] = []

        await message.delete()
        await dialog_manager.switch_to(MovieDialogSG.movies_pagination, show_mode=ShowMode.EDIT)


async def movie_overview_handler(callback: CallbackQuery, button: Button, dialog_manager: DialogManager,
                                 *args, **kwargs):
    movie_tmdb_id = callback.data.split(':')[1]

    logging.info(f"Movie overview handler: {movie_tmdb_id}")

    dialog_manager.dialog_data["current_movie_tmdb_id"] = movie_tmdb_id

    await dialog_manager.switch_to(MovieDialogSG.movie_overview, show_mode=ShowMode.EDIT)
    await callback.answer("🎬 Movie overview")


async def go_to_previous_movie(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data["current_movie_tmdb_id"] = dialog_manager.dialog_data[
        "suggestions_depth_stack"].pop()
    await dialog_manager.switch_to(MovieDialogSG.movie_overview, show_mode=ShowMode.EDIT)
    await callback.answer("🎬 Movie overview")


async def go_to_previous_movie_suggestions(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data["current_movie_tmdb_id"] = dialog_manager.dialog_data[
        "suggestions_depth_stack"][-1]

    previous_movie_data = await get_data(f"movieoverview:{dialog_manager.dialog_data['current_movie_tmdb_id']}")
    previous_movie= Movie(**(json.loads(previous_movie_data)))
    dialog_manager.dialog_data["current_movie_pretty_title"] = previous_movie.pretty_title

    await dialog_manager.switch_to(MovieDialogSG.movie_suggestions, show_mode=ShowMode.EDIT)
    await callback.answer("🎬 Movie suggestions")


async def get_movie_overview_data(dialog_manager: DialogManager, *args, **kwargs) -> dict:
    """
    Get movie overview data from dialog manager.

    :param dialog_manager:
    :param args:
    :param kwargs:
    :return:  Movie overview data.

    """
    movie_tmdb_id = dialog_manager.dialog_data["current_movie_tmdb_id"]
    redis_key = f"movieoverview:{movie_tmdb_id}"

    if await is_exist(redis_key):
        logging.info(f"Retrieving data from Redis by key: {redis_key}")
        cache = await get_data(redis_key)
        movie = Movie(**(json.loads(cache)))
    else:
        logging.info(f"Making a API request to TMDB API by movie id: {movie_tmdb_id}")
        movie = Movie(tmdb_id=movie_tmdb_id)
        await get_movie_details_tmdb(movie)
        if movie.imdb_id:
            await get_movie_details_omdb(movie)
        logging.info("Movie details: " + movie.json_data)
        await set_data(redis_key, movie.json_data)

    dialog_manager.dialog_data["current_movie_pretty_title"] = movie.pretty_title
    dump_data = movie.model_dump()
    return dump_data


async def get_list_of_keyboard_movies(dialog_manager: DialogManager, *args, **kwargs) -> dict:
    user_request = dialog_manager.dialog_data["user_request"]
    dialog_manager.dialog_data["current_movie_tmdb_id"] = None

    redis_key = f"keybmovies:{user_request.lower().replace(' ', '')}"

    if await is_exist(redis_key):
        logging.info(f"Retrieving data from Redis by key: {redis_key}")
        cache = await get_data(redis_key)
        keyboard_movies = [KeyboardMovie(**(json.loads(item)))
                           for item in cache]
    else:
        logging.info(f"Making a API request to TMDB API by title: {user_request}")
        keyboard_movies = await get_movies_by_title(user_request)
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


async def previous_page_handler(callback: CallbackQuery, message_input: MessageInput, manager: DialogManager):
    logging.info("Previous page handler")
    if manager.dialog_data["current_keyboard_movies_page"] > 1:
        manager.dialog_data["current_keyboard_movies_page"] -= 1
    await manager.update(data=manager.dialog_data, show_mode=ShowMode.EDIT)
    await callback.answer("Page " + keys_emojis[manager.dialog_data["current_keyboard_movies_page"]])


async def next_page_handler(callback: CallbackQuery, message_input: MessageInput, manager: DialogManager):
    logging.info("Next page handler")
    if (manager.dialog_data["current_keyboard_movies_page"] <
            manager.dialog_data["total_number_of_keyboard_movies_pages"]):
        manager.dialog_data["current_keyboard_movies_page"] += 1
    await manager.update(data=manager.dialog_data, show_mode=ShowMode.EDIT)
    await callback.answer("Page " + keys_emojis[manager.dialog_data["current_keyboard_movies_page"]])


async def movie_suggestions_handler(callback: CallbackQuery, button: Button, dialog_manager: DialogManager,
                                    *args, **kwargs):
    logging.info("Movie suggestions handler")
    dialog_manager.dialog_data["current_keyboard_movies_page"] = 1

    dialog_manager.dialog_data["suggestions_depth_stack"].append(
        dialog_manager.dialog_data["current_movie_tmdb_id"])

    await dialog_manager.switch_to(MovieDialogSG.movie_suggestions, show_mode=ShowMode.EDIT)
    await callback.answer("🎬 Movie suggestions")


async def get_list_of_movie_suggestions(dialog_manager: DialogManager, *args, **kwargs) -> dict:
    current_movie_tmdb_id = dialog_manager.dialog_data["current_movie_tmdb_id"]

    redis_key = f"keybmoviesuggestions:{current_movie_tmdb_id}"

    if await is_exist(redis_key):
        logging.info(f"Retrieving data from Redis by key: {redis_key}")
        cache = await get_data(redis_key)
        suggestions = [KeyboardMovie(**(json.loads(item))) for item in cache]
    else:
        logging.info(f"Making a API request to TMDB API by movie id: {current_movie_tmdb_id}")
        suggestions = await get_suggestions_by_id(current_movie_tmdb_id)
        cache = [movie.json_data for movie in suggestions]
        await set_data(redis_key, cache)

    number_of_pages = math.ceil(len(suggestions) / 10)

    dialog_manager.dialog_data["total_number_of_keyboard_movies_pages"] = number_of_pages

    keyboard_movies = suggestions[(dialog_manager.dialog_data["current_keyboard_movies_page"] - 1) * 10:
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


async def message_handler(message: Message, message_input: MessageInput, dialog_manager: DialogManager):
    logging.info(f"Message from '{message.from_user.username}' received: '{message.text}'")
    dialog_manager.show_mode = ShowMode.EDIT
    await message.delete()


async def unknown_message_handler(message: Message, *args):
    await message.answer(text=unknown_type_message, parse_mode="HTML")
