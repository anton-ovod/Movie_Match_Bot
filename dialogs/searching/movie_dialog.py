from aiogram.types import ContentType
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel, SwitchTo
from aiogram_dialog.widgets.text import Const, Jinja

from dialogs.searching import env
from handlers.messages_handlers import message_handler
from handlers.searching_handlers import subject_title_request_handler
from keyboards.searching_keyboards import get_base_subjects_keyboard, get_base_subjects_navigation_keyboard, \
    get_subject_overview_keyboard

from getters.searching_dialogs_getters import (get_list_of_found_base_subjects_by_title, get_subject_overview_by_id,
                                               get_list_of_subject_suggestions_by_id)
from misc.states import MovieDialogSG

title_request_message = env.get_template("movie/movie_search_message.jinja2")
results_message = env.get_template("common/results_message.jinja2")
movie_overview_message = env.get_template("movie/movie_overview_message.jinja2")
movie_suggestions_message = env.get_template("movie/movie_suggestions_message.jinja2")
movie_availability_message = env.get_template("movie/movie_availability_message.jinja2")
no_results_message = env.get_template("common/no_results_message.jinja2").render()

movie_dialog = Dialog(
    Window(
        Jinja(title_request_message),
        Cancel(Const("⬅️  Back")),
        MessageInput(subject_title_request_handler, content_types=[ContentType.TEXT]),
        parse_mode="HTML",
        state=MovieDialogSG.TITLE_REQUEST,
        disable_web_page_preview=True
    ),
    Window(
        Jinja(results_message,
              when=lambda movie_data, _, __: movie_data.get("base_subjects")),
        Jinja(no_results_message,
              when=lambda movie_data, _, __: not movie_data.get("base_subjects")),
        get_base_subjects_keyboard(),
        get_base_subjects_navigation_keyboard(),
        MessageInput(message_handler),
        getter=get_list_of_found_base_subjects_by_title,
        state=MovieDialogSG.BASE_MOVIES_PAGINATION,
        parse_mode="HTML",
        disable_web_page_preview=True
    ),
    Window(
        Jinja(movie_overview_message),
        get_subject_overview_keyboard(),
        MessageInput(message_handler),
        state=MovieDialogSG.MOVIE_OVERVIEW,
        getter=get_subject_overview_by_id,
        parse_mode="HTML",
    ),
    Window(
        Jinja(movie_suggestions_message),
        get_base_subjects_keyboard(),
        get_base_subjects_navigation_keyboard(),
        MessageInput(message_handler),
        getter=get_list_of_subject_suggestions_by_id,
        state=MovieDialogSG.MOVIE_SUGGESTIONS,
        parse_mode="HTML",
        disable_web_page_preview=True
    ),
    Window(
        Jinja(movie_availability_message),
        SwitchTo(
            Const("⬅️  Back"),
            id="overview",
            state=MovieDialogSG.MOVIE_OVERVIEW
        ),
        MessageInput(message_handler),
        getter=get_subject_overview_by_id,
        state=MovieDialogSG.MOVIE_AVAILABILITY,
        parse_mode="HTML",
        disable_web_page_preview=True
    ),
)
