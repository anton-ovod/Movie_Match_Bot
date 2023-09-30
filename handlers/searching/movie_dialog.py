import logging

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button

from dialogs.searching.movie_dialog import MovieDialogSG, movie_dialog

movie_search_router = Router()
movie_search_router.include_router(movie_dialog)


async def init_movie_search_dialog(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    logging.info("Movie search dialog initialized")
    await dialog_manager.start(MovieDialogSG.title_request, show_mode=ShowMode.EDIT)
    await callback.answer("🔍  Search » 🎬  Movie")


@movie_search_router.message(MovieDialogSG.title_request)
async def message_handler(message: Message):
    logging.info(f"Message from '{message.from_user.username}' received: '{message.text}'")

