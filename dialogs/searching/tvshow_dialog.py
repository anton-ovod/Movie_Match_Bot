from aiogram.enums import ContentType


from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Group, SwitchTo, Row, Cancel, Back
from aiogram_dialog.widgets.text import Const, Jinja, Format

from aiogram_dialog import Dialog

from getters.searching_dialogs_getters import get_list_of_found_base_subjects_by_title
from handlers.messages_handlers import message_handler, unknown_message_handler
from handlers.searching_handlers import subject_title_request_handler

from dialogs.searching import env
from keyboards.searching_keyboards import get_base_subjects_keyboard, get_base_subjects_navigation_keyboard

from misc.states import TVShowDialogSG

tvshow_title_request_message = env.get_template("tvshow/tvshow_search_message.jinja2").render()
results_message = env.get_template("common/results_message.jinja2")
no_results_message = env.get_template("common/no_results_message.jinja2").render()

tvshow_dialog = Dialog(
    Window(
        Jinja(tvshow_title_request_message),
        Cancel(Const("⬅️  Back"),
               on_click=lambda callback, self, manager: callback.answer("🔍 Search")),
        MessageInput(subject_title_request_handler, content_types=[ContentType.TEXT]),
        MessageInput(unknown_message_handler),
        state=TVShowDialogSG.TITLE_REQUEST,
        parse_mode="HTML",
        disable_web_page_preview=True,
    ),
    Window(
        Jinja(results_message,
              when=lambda result_data, _, __: result_data.get("base_subjects")),
        Jinja(no_results_message,
              when=lambda result_data, _, __: not result_data.get("base_subjects")),
        get_base_subjects_keyboard(),
        get_base_subjects_navigation_keyboard(),
        MessageInput(message_handler),
        getter=get_list_of_found_base_subjects_by_title,
        state=TVShowDialogSG.BASE_TVSHOWS_PAGINATION,
        parse_mode="HTML",
        disable_web_page_preview=True
    ),
)
