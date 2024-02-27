import logging

from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from misc.states import ShowDialogSG
from dialogs.searching import env

tvshow_search_router = Router()

unknown_type_message = env.get_template("common/unknown_type_message.jinja2").render()


async def init_tvshow_search_dialog(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    logging.info("TV show search dialog initialized")
    await dialog_manager.start(ShowDialogSG.title_request, show_mode=ShowMode.EDIT)
    await callback.answer("🤖 I'm ready to search for tv show!")


async def title_request_handler(message: Message, message_input: MessageInput,
                                dialog_manager: DialogManager):
    if not message.html_text.isascii():
        await message.answer(text=unknown_type_message, parse_mode="HTML")
    else:
        dialog_manager.dialog_data["user_request"] = message.text
        logging.info(f"[TV show search] User request: `{message.text}` successfully saved")

        dialog_manager.dialog_data["current_keyboard_movies_page"] = 1
        if "suggestions_depth_stack" not in dialog_manager.dialog_data:
            dialog_manager.dialog_data["suggestions_depth_stack"] = []

        await message.delete()
        await dialog_manager.switch_to(ShowDialogSG.shows_pagination, show_mode=ShowMode.EDIT)


async def unknown_message_handler(message: Message, *args):
    await message.answer(text=unknown_type_message, parse_mode="HTML")
