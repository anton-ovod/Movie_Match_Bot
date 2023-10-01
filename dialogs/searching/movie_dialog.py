import logging

from aiogram.filters.state import State, StatesGroup
from aiogram.types import Message, ContentType

from aiogram_dialog import Window, DialogManager, Dialog, ShowMode
from aiogram_dialog.widgets.kbd import Back, Cancel
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const, Format

from dialogs.searching import env

title_request_message = env.get_template("movie_message.jinja2").render()
unknown_type_message = env.get_template("unknown_type_message.jinja2").render()
results_message = env.get_template("results_message.jinja2")


class MovieDialogSG(StatesGroup):
    title_request = State()
    movies_pagination = State()
    movie_overview = State()


async def title_request_handler(message: Message, message_input: MessageInput,
                                dialog_manager: DialogManager):
    dialog_manager.dialog_data["user_request"] = message.text
    logging.info(f"User request: `{message.text}` successfully saved")
    await message.delete()
    await dialog_manager.switch_to(MovieDialogSG.movies_pagination, show_mode=ShowMode.EDIT)


async def unknown_message_handler(message: Message, *args):
    await message.answer(text=unknown_type_message, parse_mode="HTML")


movie_dialog = Dialog(
    Window(
        title_request_message,
        Cancel(Const("⬅️  Back"),
               on_click=lambda callback, self, manager: callback.answer("🔍 Search")),
        MessageInput(title_request_handler, content_types=[ContentType.TEXT]),
        MessageInput(unknown_message_handler),
        parse_mode="HTML",
        state=MovieDialogSG.title_request,
        disable_web_page_preview=True
    ),
    Window(
        results_message.render(title_request="{dialog_data[user_request]}"),
        Back(text=Const("⬅️  Back")),
        state=MovieDialogSG.movies_pagination,
        parse_mode="HTML",
        disable_web_page_preview=True
    )
)
