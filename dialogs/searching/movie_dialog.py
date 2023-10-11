import operator

from aiogram.types import ContentType
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Back, Cancel, Group, Select, Row, Column
from aiogram_dialog.widgets.text import Const, Format

from dialogs.searching import env
from handlers.searching.movie_dialog import (title_request_handler, unknown_message_handler, message_handler,
                                             get_list_of_keyboard_movies, movie_overview_handler)
from misc.states import MovieDialogSG

title_request_message = env.get_template("movie_message.jinja2").render()
results_message = env.get_template("results_message.jinja2")

keyboard_movies_group = Group(
    Column(
        Select(
            Format("{item.pretty_title}"),
            id="keyboard_movies",
            item_id_getter=operator.itemgetter("tmdb_id"),
            items="keyboard_movies",
            on_click=movie_overview_handler,
        )
    ),
    Row(
        Back(text=Const("⬅️  Back"))
    )
)
movie_dialog = Dialog(
    Window(
        title_request_message,
        Cancel(Const("⬅️  Back"),
               on_click=lambda callback, self, manager: callback.answer("🔍 Search")),
        MessageInput(title_request_handler, content_types=[ContentType.TEXT]),
        MessageInput(func=unknown_message_handler),
        parse_mode="HTML",
        state=MovieDialogSG.title_request,
        disable_web_page_preview=True
    ),
    Window(
        results_message.render(title_request="{dialog_data[user_request]}"),
        keyboard_movies_group,
        MessageInput(message_handler),
        getter=get_list_of_keyboard_movies,
        state=MovieDialogSG.movies_pagination,
        parse_mode="HTML",
        disable_web_page_preview=True
    )
)
