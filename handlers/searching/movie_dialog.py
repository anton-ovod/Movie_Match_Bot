import logging

from aiogram import Router, Bot
from aiogram.types import CallbackQuery, Message

from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from misc.states import MovieDialogSG

from utils.caching_handlers import get_data, set_data, is_exist
from utils.imdb_api import get_movies_by_title

from dialogs.searching import env

movie_search_router = Router()

unknown_type_message = env.get_template("unknown_type_message.jinja2").render()


async def init_movie_search_dialog(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    logging.info("Movie search dialog initialized")
    await dialog_manager.start(MovieDialogSG.title_request, show_mode=ShowMode.EDIT)
    await callback.answer("🤖 I'm ready to search for movies!")


async def title_request_handler(message: Message, message_input: MessageInput,
                                dialog_manager: DialogManager):
    dialog_manager.dialog_data["user_request"] = message.text
    logging.info(f"User request: `{message.text}` successfully saved")

    redis_key = f"keybmovies:{message.text.strip().lower()}"

    if await is_exist(redis_key):
        keyboard_movies = await get_data(redis_key)
    else:
        keyboard_movies = await get_movies_by_title(message.text)
        await set_data(redis_key, keyboard_movies)

    # dialog_manager.dialog_data["current_keyboard_movies"] = keyboard_movies
    logging.info(f"Keyboard movies: {keyboard_movies}")
    await message.delete()
    await dialog_manager.switch_to(MovieDialogSG.movies_pagination, show_mode=ShowMode.EDIT)


async def unknown_message_handler(message: Message, *args):
    await message.answer(text=unknown_type_message, parse_mode="HTML")
