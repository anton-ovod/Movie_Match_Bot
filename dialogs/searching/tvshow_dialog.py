from aiogram.enums import ContentType
from aiogram.filters.state import State, StatesGroup

from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Group, SwitchTo, Row, Cancel, Back
from aiogram_dialog.widgets.text import Const, Jinja, Format

from aiogram_dialog import Dialog

from handlers.searching.tvshow_dialog import title_request_handler, unknown_message_handler

from dialogs.searching import env

from misc.states import ShowDialogSG

tvshow_title_request_message = env.get_template("tvshow/tvshow_search_message.jinja2").render()

tvshow_dialog = Dialog(
    Window(
        Jinja(tvshow_title_request_message),
        Cancel(Const("⬅️  Back"),
               on_click=lambda callback, self, manager: callback.answer("🔍 Search")),
        MessageInput(title_request_handler, content_types=[ContentType.TEXT]),
        MessageInput(unknown_message_handler),
        state=ShowDialogSG.title_request,
        parse_mode="HTML",
        disable_web_page_preview=True,
    ),
    Window(
        Format("User request: `{dialog_data[user_request]}` successfully saved"),
        Back(Const("⬅️  Back")),
        state=ShowDialogSG.shows_pagination,
        parse_mode="HTML",
        disable_web_page_preview=True
    )
)
