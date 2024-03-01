import logging
import operator
import emoji

from aiogram.types import ContentType
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Back, Cancel, Group, Select, Row, Column, Button, Url, SwitchTo
from aiogram_dialog.widgets.text import Const, Format, Jinja

from dialogs.searching import env
from handlers.searching.common_handlers import unknown_message_handler, message_handler
from handlers.searching.movie_dialog import (title_request_handler,
                                             get_list_of_found_movies, movie_overview_handler, next_page_handler,
                                             previous_page_handler, get_movie_overview_data, movie_suggestions_handler,
                                             get_list_of_movie_suggestions, go_to_previous_movie,
                                             go_to_previous_movie_suggestions)
from misc.states import MovieDialogSG

title_request_message = env.get_template("movie/movie_search_message.jinja2")
results_message = env.get_template("common/results_message.jinja2")
movie_overview_message = env.get_template("movie/movie_overview_message.jinja2")
movie_suggestions_message = env.get_template("movie/movie_suggestions_message.jinja2")
movie_availability_message = env.get_template("movie/movie_availability_message.jinja2")
no_results_message = env.get_template("common/no_results_message.jinja2").render()



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
        Back(Const("⬅️  Back"),
             on_click=lambda callback, self, manager:
             callback.answer("🤖 I'm ready to search for movies!"),
             when=lambda _, __, dialog_manager:
             not dialog_manager.dialog_data["suggestions_depth_stack"]
             ),
        Button(Const("⬅️  Back"), id="back",
               on_click=go_to_previous_movie,
               when=lambda _, __, dialog_manager:
               dialog_manager.dialog_data["suggestions_depth_stack"]
               ),
        when=lambda _, __, dialog_manager:
        dialog_manager.dialog_data["total_number_of_keyboard_movies_pages"] == 1
    ),

    Row(
        Back(Const("⬅️  Back"),
             on_click=lambda callback, self, manager:
             callback.answer("🤖 I'm ready to search for movies!"),
             when=lambda _, __, dialog_manager:
             not dialog_manager.dialog_data["suggestions_depth_stack"]
             ),
        Button(Const("⬅️  Back"), id="back",
               on_click=go_to_previous_movie,
               when=lambda _, __, dialog_manager:
               dialog_manager.dialog_data["suggestions_depth_stack"]
               ),
        Cancel(Const("🕵️ Search"), id="search",
               on_click=lambda callback, self, manager: callback.answer("🔍 Search")),
        Button(Format("{next_page}"),
               id="next_page",
               on_click=next_page_handler),
        when=lambda _, __, dialog_manager:
        dialog_manager.dialog_data["current_keyboard_movies_page"] == 1 and
        dialog_manager.dialog_data["total_number_of_keyboard_movies_pages"] > 1
    ),

    Row(
        Button(Format("{prev_page}"),
               id="prev_page",
               on_click=previous_page_handler),
        Cancel(Const("🕵️ Search"), id="search",
               on_click=lambda callback, self, manager: callback.answer("🔍 Search")),
        when=lambda _, __, dialog_manager:
        dialog_manager.dialog_data["current_keyboard_movies_page"] ==
        dialog_manager.dialog_data["total_number_of_keyboard_movies_pages"] and
        dialog_manager.dialog_data["total_number_of_keyboard_movies_pages"] > 1

    ),

    Row(
        Button(Format("{prev_page}"),
               id="prev_page",
               on_click=previous_page_handler),
        Cancel(Const("🕵️ Search"), id="search",
               on_click=lambda callback, self, manager: callback.answer("🔍 Search")),
        Button(Format("{next_page}"),
               id="next_page",
               on_click=next_page_handler),
        when=lambda _, __, dialog_manager: dialog_manager.dialog_data["current_keyboard_movies_page"] !=
                                           dialog_manager.dialog_data["total_number_of_keyboard_movies_pages"] > 1 !=
                                           dialog_manager.dialog_data["current_keyboard_movies_page"]

    )

)

movie_overview_group = Group(
    Url(
        Const("🎬 Homepage"),
        Format("{homepage}"),
        when=lambda movie_data, _, __: movie_data.get("homepage")
    ),
    Url(
        Const("🎬 Homepage"),
        Format("{imdb_url}"),
        when=lambda movie_data, _, __: not movie_data.get("homepage") and movie_data.get("imdb_url")
    ),
    Url(
        Const("🎬 Homepage"),
        Format("{tmdb_url}"),
        when=lambda movie_data, _, __: not movie_data.get("homepage") and not movie_data.get("imdb_url")
    ),
    Url(
        Const("🎞 Trailer"),
        Format("{trailer_url}"),
        when=lambda movie_data, _, __: movie_data.get("trailer_url")
    ),

    Button(Const("🗂 Suggestions"), id="suggestions",
           on_click=movie_suggestions_handler),

    SwitchTo(Const("📽 Availability"), id="availability",
             on_click=lambda callback, self, manager: callback.answer("📽 Availability"),
             state=MovieDialogSG.movie_availability),

    Back(Const("⬅️  Back"),
         on_click=lambda callback, self, manager: callback.answer("🔍 Search"),
         when=lambda _, __, dialog_manager: not dialog_manager.dialog_data["suggestions_depth_stack"]
         ),

    Button(Const("⬅️  Back"),
           id="back",
           on_click=go_to_previous_movie_suggestions,
           when=lambda _, __, dialog_manager: dialog_manager.dialog_data["suggestions_depth_stack"]
           ),

    Button(Const("🤲 Share"), id="share",
           on_click=lambda callback, self, manager: callback.answer("🤲 Share")),

    width=2
)

movie_dialog = Dialog(
    Window(
        Jinja(title_request_message),
        Cancel(Const("⬅️  Back"),
               on_click=lambda callback, self, manager: callback.answer("🔍 Search")),
        MessageInput(title_request_handler, content_types=[ContentType.TEXT]),
        MessageInput(unknown_message_handler),
        parse_mode="HTML",
        state=MovieDialogSG.title_request,
        disable_web_page_preview=True
    ),
    Window(
        Jinja(results_message,
              when=lambda movie_data, _, __: movie_data.get("keyboard_movies")),
        Jinja(no_results_message,
              when=lambda movie_data, _, __: not movie_data.get("keyboard_movies")),
        keyboard_movies_group,
        keyboard_movies_navigation_group,
        MessageInput(message_handler),
        getter=get_list_of_found_movies,
        state=MovieDialogSG.movies_pagination,
        parse_mode="HTML",
        disable_web_page_preview=True
    ),
    Window(
        Jinja(movie_overview_message),
        movie_overview_group,
        MessageInput(message_handler),
        state=MovieDialogSG.movie_overview,
        getter=get_movie_overview_data,
        parse_mode="HTML",
    ),
    Window(
        Jinja(movie_suggestions_message),
        keyboard_movies_group,
        keyboard_movies_navigation_group,
        MessageInput(message_handler),
        getter=get_list_of_movie_suggestions,
        state=MovieDialogSG.movie_suggestions,
        parse_mode="HTML",
        disable_web_page_preview=True
    ),
    Window(
        Jinja(movie_availability_message),
        SwitchTo(Const("⬅️  Back"), id="overview",
                 on_click=lambda callback, self, manager: callback.answer("🎬 Overview"),
                 state=MovieDialogSG.movie_overview),
        MessageInput(message_handler),
        getter=get_movie_overview_data,
        state=MovieDialogSG.movie_availability,
        parse_mode="HTML",
        disable_web_page_preview=True
    ),
)
