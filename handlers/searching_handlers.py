import json
import logging
from aiogram import Router

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button

from handlers.messages_handlers import unknown_message_handler
from misc.enums import PaginationLocation, StatesGroups, SubjectsModels
from utils.caching_handlers import get_data

navigation_emoji = r"\u003{number_of_page:}\uFE0F\u20E3"  # DO NOT MAKE MORE THAN 9 PAGES
ITEMS_PER_PAGE = 7

searching_router = Router()


async def subject_title_request_handler(message: Message,
                                        _,
                                        dialog_manager: DialogManager) -> None:
    if not message.html_text.isascii():
        await unknown_message_handler(message)
    else:
        dialog_manager.dialog_data["user_request"] = message.text
        dialog_manager.dialog_data["pagination_location"] = PaginationLocation.MAIN.value
        dialog_manager.dialog_data["main_pagination_current_page"] = 1

        if "suggestions_depth_stack" not in dialog_manager.dialog_data:
            dialog_manager.dialog_data["suggestions_depth_stack"] = []

        subject_type = dialog_manager.dialog_data["subject_type"]
        subject_states_group = getattr(StatesGroups, subject_type).value

        base_subjects_pagination_state = getattr(subject_states_group,
                                                 f"BASE_{subject_type}S_PAGINATION")

        await dialog_manager.switch_to(state=base_subjects_pagination_state,
                                       show_mode=ShowMode.EDIT)

        await message.delete()


async def subject_overview_handler(callback: CallbackQuery,
                                   _,
                                   dialog_manager: DialogManager,
                                   *args
                                   ) -> None:
    subject_tmdb_id = callback.data.split(':')[1]
    subject_type = dialog_manager.dialog_data["subject_type"]

    logging.info(f"{subject_type.lower()} overview handler: {subject_tmdb_id}")

    dialog_manager.dialog_data[f"current_{subject_type.lower()}_tmdb_id"] = subject_tmdb_id

    subject_states_group = getattr(StatesGroups, subject_type).value

    subject_overview_state = getattr(subject_states_group,
                                     f"{subject_type}_OVERVIEW")

    await dialog_manager.switch_to(state=subject_overview_state, show_mode=ShowMode.EDIT)


async def subject_suggestions_handler(_,
                                      __,
                                      dialog_manager: DialogManager,
                                      *args,
                                      **kwargs):
    dialog_manager.dialog_data["pagination_location"] = PaginationLocation.SUGGESTIONS.value
    dialog_manager.dialog_data["suggestions_pagination_current_page"] = 1
    subject_type = dialog_manager.dialog_data["subject_type"]

    dialog_manager.dialog_data["suggestions_depth_stack"].append(
        dialog_manager.dialog_data[f"current_{subject_type.lower()}_tmdb_id"])

    subject_states_group = getattr(StatesGroups, subject_type).value

    subject_suggestions_state = getattr(subject_states_group,
                                        f"{subject_type}_SUGGESTIONS")

    await dialog_manager.switch_to(subject_suggestions_state, show_mode=ShowMode.EDIT)


async def subject_availability_handler(_,
                                       __,
                                       dialog_manager: DialogManager,
                                       *args,
                                       **kwargs):
    subject_type = dialog_manager.dialog_data["subject_type"]

    subject_states_group = getattr(StatesGroups, subject_type).value

    subject_availability_state = getattr(subject_states_group,
                                         f"{subject_type}_AVAILABILITY")

    await dialog_manager.switch_to(subject_availability_state, show_mode=ShowMode.EDIT)


async def pagination_handler(callback: CallbackQuery,
                             button: Button,
                             manager: DialogManager):
    pagination_location = manager.dialog_data["pagination_location"]
    current_page = manager.dialog_data[f"{pagination_location}_pagination_current_page"]
    total_pages = manager.dialog_data[f"total_{pagination_location}_pagination_pages"]

    direction = 1 if button.widget_id == "next_page" else -1
    current_page += direction

    if current_page < 1:
        current_page = 1
    elif current_page > total_pages:
        current_page = total_pages

    manager.dialog_data[f"{pagination_location}_pagination_current_page"] = current_page

    await callback.answer("Page " + navigation_emoji.format(
        number_of_page=manager.dialog_data[f"{pagination_location}_pagination_current_page"]).encode('utf-8').
                          decode('unicode-escape'))


async def previous_movie_overview_handler(_,
                                          __,
                                          dialog_manager: DialogManager):
    subject_type = dialog_manager.dialog_data["subject_type"]

    dialog_manager.dialog_data[f"current_{subject_type.lower()}_tmdb_id"] = (
        dialog_manager.dialog_data["suggestions_depth_stack"].pop())

    subject_states_group = getattr(StatesGroups, subject_type).value

    subject_overview_state = getattr(subject_states_group,
                                     f"{subject_type}_OVERVIEW")

    await dialog_manager.switch_to(subject_overview_state, show_mode=ShowMode.EDIT)


async def previous_movie_suggestions_handler(_,
                                             __,
                                             dialog_manager: DialogManager):
    subject_type = dialog_manager.dialog_data["subject_type"]
    subject_class = getattr(SubjectsModels, subject_type).detailed_class

    dialog_manager.dialog_data[f"current_{subject_type.lower()}_tmdb_id"] = (
        dialog_manager.dialog_data)["suggestions_depth_stack"][-1]

    current_tmdb_id = dialog_manager.dialog_data[f"current_{subject_type.lower()}_tmdb_id"]
    redis_key = f"{subject_type.lower()}:overview:{current_tmdb_id}"

    previous_movie_data = await get_data(redis_key)
    previous_movie = subject_class(**(json.loads(previous_movie_data)))

    dialog_manager.dialog_data["current_movie_pretty_title"] = previous_movie.pretty_title

    subject_states_group = getattr(StatesGroups, subject_type).value

    subject_suggestions_state = getattr(subject_states_group,
                                        f"{subject_type}_SUGGESTIONS")

    await dialog_manager.switch_to(subject_suggestions_state, show_mode=ShowMode.EDIT)
