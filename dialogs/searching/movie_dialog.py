import operator

from aiogram.types import ContentType
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Back, Cancel, Group, Select, Row, Column, SwitchTo, Button
from aiogram_dialog.widgets.text import Const, Format

from dialogs.searching import env
from handlers.searching.movie_dialog import (title_request_handler, unknown_message_handler, message_handler,
                                             get_list_of_keyboard_movies, movie_overview_handler, next_page_handler,
                                             previous_page_handler)
from misc.states import MovieDialogSG, HomeDialogSG

title_request_message = env.get_template("movie_message.jinja2").render()
results_message = env.get_template("results_message.jinja2")

keys_emojis = {
    "1": "1️⃣",
    "2": "2️⃣",
    "3": "3️⃣",
    "4": "4️⃣",
    "5": "5️⃣",
    "6": "6️⃣",
    "7": "7️⃣",
    "8": "8️⃣",
    "9": "9️⃣",
    "10": "🔟",
}

keyboard_movies_group = Group(
    Column(
        Select(
            Format("{item.pretty_title}"),
            id="keyboard_movies",
            item_id_getter=operator.itemgetter("tmdb_id"),
            items="keyboard_movies",
            on_click=movie_overview_handler,
        )
    )
)

keyboard_movies_navigation_group = Group(

    Row(
        Back(Const("⬅️  Back"), id="back",
             on_click=lambda callback, self, manager: callback.answer("🤖 I'm ready to search for movies!")
             ),
        when=lambda _, __, dialog_manager: dialog_manager.dialog_data["total_number_of_keyboard_movies"] == 1

    ),

    Row(
        Back(Const("⬅️  Back"), id="back",
             on_click=lambda callback, self, manager: callback.answer("🤖 I'm ready to search for movies!")),
        Cancel(Const("🕵️ Search"), id="search",
               on_click=lambda callback, self, manager: callback.answer("🔍 Search")),
        Button(Const(keys_emojis[Format("{next_page}").text]), id="next_page", on_click=next_page_handler),
        when=lambda _, __, dialog_manager: dialog_manager.dialog_data["current_keyboard_movies_page"] == 1
    ),

    Row(
        Button(Const(keys_emojis[Format("{prev_page}").text]), id="prev_page", on_click=previous_page_handler),
        Cancel(Const("🕵️ Search"), id="search",
               on_click=lambda callback, self, manager: callback.answer("🔍 Search")),
        when=lambda _, __, dialog_manager: dialog_manager.dialog_data["current_keyboard_movies_page"] ==
                                           dialog_manager.dialog_data["total_number_of_keyboard_movies"]

    ),

    Row(
        Button(Const(keys_emojis[Format("{prev_page}").text]), id="prev_page", on_click=previous_page_handler),
        Cancel(Const("🕵️ Search"), id="search",
               on_click=lambda callback, self, manager: callback.answer("🔍 Search")),
        Button(Const(keys_emojis[Format("{next_page}")]), id="next_page", on_click=next_page_handler),
        when=lambda _, __, dialog_manager: dialog_manager.dialog_data["current_keyboard_movies_page"] != dialog_manager.dialog_data["total_number_of_keyboard_movies"] > 1 !=
                                           dialog_manager.dialog_data["current_keyboard_movies_page"]

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
        results_message.render(title_request="{dialog_data[user_request]} +++ {prev_page} +++ {next_page}"),
        keyboard_movies_group,
        keyboard_movies_navigation_group,
        MessageInput(message_handler),
        getter=get_list_of_keyboard_movies,
        state=MovieDialogSG.movies_pagination,
        parse_mode="HTML",
        disable_web_page_preview=True
    )
)
