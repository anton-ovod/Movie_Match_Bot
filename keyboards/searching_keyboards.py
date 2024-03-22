import operator
from aiogram_dialog.widgets.kbd import Group, Column, Select, Keyboard, Row, Back, Button, Cancel, Url, SwitchTo
from aiogram_dialog.widgets.text import Format, Const

from handlers.searching_handlers import subject_overview_handler, pagination_handler, subject_suggestions_handler, \
    previous_movie_suggestions_handler, previous_movie_overview_handler, subject_availability_handler


def get_base_subjects_keyboard() -> Keyboard:
    base_subjects_keyboard = Group(
        Column(
            Select(
                Format("{item.pretty_title}"),
                id="base_subjects",
                item_id_getter=operator.itemgetter("tmdb_id"),
                items="base_subjects",
                on_click=subject_overview_handler
            )
        )
    )
    return base_subjects_keyboard


def get_base_subjects_navigation_keyboard() -> Keyboard:
    base_subjects_navigation_keyboard = Group(
        Row(
            Back(Const("⬅️  Back"),
                 when=lambda _, __, dialog_manager:
                 not dialog_manager.dialog_data["suggestions_depth_stack"]
                 ),
            Button(Const("⬅️  Back"), id="back",
                   on_click=previous_movie_overview_handler,
                   when=lambda dialog_data, _, dialog_manager:
                   dialog_manager.dialog_data["suggestions_depth_stack"]
                   or not dialog_data["base_subjects"]
                   ),
            when=lambda dialog_data, _, __:
            dialog_data["total_number_of_pages"] in (0, 1)
        ),

        Row(
            Back(Const("⬅️  Back"),
                 when=lambda _, __, dialog_manager:
                 not dialog_manager.dialog_data["suggestions_depth_stack"]
                 ),
            Button(Const("⬅️  Back"), id="back",
                   on_click=previous_movie_overview_handler,
                   when=lambda _, __, dialog_manager:
                   dialog_manager.dialog_data["suggestions_depth_stack"]
                   ),
            Cancel(Const("🕵️ Search"),
                   id="search"),
            Button(Format("{next_page}"),
                   id="next_page",
                   on_click=pagination_handler
                   ),
            when=lambda dialog_data, _, __:
            dialog_data["current_page"] == 1 and
            dialog_data["total_number_of_pages"] > 1
        ),

        Row(
            Button(Format("{prev_page}"),
                   id="prev_page",
                   on_click=pagination_handler
                   ),
            Cancel(Const("🕵️ Search"), id="search"),
            when=lambda dialog_data, _, __:
            dialog_data["current_page"] ==
            dialog_data["total_number_of_pages"] and
            dialog_data["total_number_of_pages"] > 1

        ),

        Row(
            Button(Format("{prev_page}"),
                   id="prev_page",
                   on_click=pagination_handler
                   ),
            Cancel(Const("🕵️ Search"), id="search"),
            Button(Format("{next_page}"),
                   id="next_page",
                   on_click=pagination_handler
                   ),
            when=lambda dialog_data, _, __:
            dialog_data["current_page"] !=
            dialog_data["total_number_of_pages"] > 1 !=
            dialog_data["current_page"]
        )
    )
    return base_subjects_navigation_keyboard


def get_subject_overview_keyboard() -> Keyboard:
    subject_overview_buttons = Group(
        Url(
            Const("🎬 Homepage"),
            Format("{homepage}"),
            when=lambda movie_data, _, __: movie_data.get("homepage")
        ),
        Url(
            Const("🎬 Homepage"),
            Format("{imdb_url}"),
            when=lambda movie_data, _, __:
            not movie_data.get("homepage") and movie_data.get("imdb_url")
        ),
        Url(
            Const("🎬 Homepage"),
            Format("{tmdb_url}"),
            when=lambda movie_data, _, __:
            not movie_data.get("homepage") and not movie_data.get("imdb_url")
        ),
        Url(
            Const("🎞 Trailer"),
            Format("{trailer_url}"),
            when=lambda movie_data, _, __: movie_data.get("trailer_url")
        ),

        Button(
            Const("🗂 Suggestions"),
            id="suggestions",
            on_click=subject_suggestions_handler),

        Button(
            Const("📽 Availability"),
            id="availability",
            on_click=subject_availability_handler),

        Back(
            Const("⬅️  Back"),
            when=lambda _, __, dialog_manager:
            not dialog_manager.dialog_data["suggestions_depth_stack"]
        ),

        Button(Const("⬅️  Back"),
               id="back",
               on_click=previous_movie_suggestions_handler,
               when=lambda _, __, dialog_manager:
               dialog_manager.dialog_data["suggestions_depth_stack"]
               ),

        Button(Const("🤲 Share"), id="share",
               on_click=
               lambda callback, button, manager:
               callback.answer("Share this movie with your friends!")
               ),


        width=2
    )
    return subject_overview_buttons
