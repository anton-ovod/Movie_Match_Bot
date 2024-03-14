from aiogram.enums import ContentType


from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Group, SwitchTo, Row, Cancel, Back
from aiogram_dialog.widgets.text import Const, Jinja, Format

from aiogram_dialog import Dialog

from handlers.messages_handlers import message_handler, unknown_message_handler

from dialogs.searching import env

from misc.states import TVShowDialogSG

tvshow_title_request_message = env.get_template("tvshow/tvshow_search_message.jinja2").render()
results_message = env.get_template("common/results_message.jinja2")
no_results_message = env.get_template("common/no_results_message.jinja2").render()

tvshow_dialog = Dialog(
    Window(
        Jinja(tvshow_title_request_message),
        Cancel(Const("⬅️  Back"),
               on_click=lambda callback, self, manager: callback.answer("🔍 Search")),
        #MessageInput(title_request_handler, content_types=[ContentType.TEXT]),
        #MessageInput(unknown_message_handler),
        state=TVShowDialogSG.TITLE_REQUEST,
        parse_mode="HTML",
        disable_web_page_preview=True,
    ),
    Window(
        Jinja(results_message,
              when=lambda movie_data, _, __: movie_data.get("base_movies")),
        Jinja(no_results_message,
              when=lambda movie_data, _, __: not movie_data.get("base_movies")),
        Back(Const("⬅️  Back"),
             on_click=lambda callback, self, manager: callback.answer("🔍 Search")),
        MessageInput(message_handler),
        state=TVShowDialogSG.BASE_TVSHOWS_PAGINATION,
        parse_mode="HTML",
        disable_web_page_preview=True
    ),
)
