from aiogram.filters.state import State, StatesGroup

from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Group, SwitchTo, Row, Cancel
from aiogram_dialog.widgets.text import Const

from aiogram_dialog import Dialog

from dialogs.searching import env

title_request_message = env.get_template("movie_message.jinja2").render()


class MovieDialogSG(StatesGroup):
    title_request = State()


movie_dialog = Dialog(
    Window(
        title_request_message,
        Cancel(Const("⬅️  Back"),
               on_click=lambda callback, self, manager: callback.answer("🔍 Search")),
        parse_mode="HTML",
        state=MovieDialogSG.title_request,
        disable_web_page_preview=True
    )
)
