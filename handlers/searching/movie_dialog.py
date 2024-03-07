import json
import logging
import math

from aiogram import Router
from aiogram.types import CallbackQuery, Message

from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button

from handlers.searching.common_handlers import (get_list_of_found_base_subjects_by_title,
                                                calculate_pagination, subject_title_request_handler,
                                                pagination_handler, get_subject_overview_by_id,
                                                get_list_of_subject_suggestions_by_id,
                                                suggestions_previous_movie_handler, previous_movie_suggestions_handler)
from misc.states import MovieDialogSG
from misc.enums import TypeOfSubject, PaginationDirection, PaginationLocation

from utils.caching_handlers import get_data
from models.movie import Movie

movie_search_router = Router()

ITEMS_PER_PAGE = 7
navigation_emoji = r"\u003{number_of_page:}\uFE0F\u20E3"  # DO NOT MAKE MORE THAN 9 PAGES


async def init_movie_search_dialog(callback: CallbackQuery, _, dialog_manager: DialogManager):
    logging.info("Movie search dialog initialized")
    await dialog_manager.start(MovieDialogSG.title_request, show_mode=ShowMode.EDIT)
    await callback.answer("🤖 I'm ready to search for movies!")


async def title_request_handler(message: Message, _, dialog_manager: DialogManager):
    await subject_title_request_handler(message, dialog_manager)

    dialog_manager.dialog_data["pagination_location"] = PaginationLocation.main.value
    dialog_manager.dialog_data["main_pagination_current_page"] = 1

    await dialog_manager.switch_to(MovieDialogSG.movies_pagination, show_mode=ShowMode.EDIT)

    await message.delete()


async def get_list_of_found_movies(dialog_manager: DialogManager, *args, **kwargs) -> dict:
    user_request = dialog_manager.dialog_data["user_request"]
    dialog_manager.dialog_data["current_movie_tmdb_id"] = None
    dialog_manager.dialog_data["pagination_location"] = PaginationLocation.main.value

    base_movies = await get_list_of_found_base_subjects_by_title(user_request, TypeOfSubject.movie)

    current_base_movies_page = dialog_manager.dialog_data["main_pagination_current_page"]

    total_number_of_pages = math.ceil(len(base_movies) / ITEMS_PER_PAGE)

    dialog_manager.dialog_data["total_main_pagination_pages"] = total_number_of_pages

    next_page_number, prev_page_number = await calculate_pagination(current_base_movies_page, total_number_of_pages)

    return {
        "base_movies": base_movies[(current_base_movies_page - 1) * ITEMS_PER_PAGE:
                                   current_base_movies_page * ITEMS_PER_PAGE],
        "next_page": navigation_emoji.format(number_of_page=next_page_number).encode('utf-8').decode('unicode-escape'),
        "prev_page": navigation_emoji.format(number_of_page=prev_page_number).encode('utf-8').decode('unicode-escape'),
        "current_page": current_base_movies_page,
        "total_number_of_pages": total_number_of_pages
    }


async def base_movies_previous_page_handler(callback: CallbackQuery, _, manager: DialogManager):
    await pagination_handler(manager, PaginationDirection.previous)
    pagination_location = manager.dialog_data["pagination_location"]
    await callback.answer("Page " + navigation_emoji.format(
        number_of_page=manager.dialog_data[f"{pagination_location}_pagination_current_page"]).encode('utf-8').
                          decode('unicode-escape'))


async def base_movies_next_page_handler(callback: CallbackQuery, _, manager: DialogManager):
    await pagination_handler(manager, PaginationDirection.next)
    pagination_location = manager.dialog_data["pagination_location"]
    await callback.answer("Page " + navigation_emoji.format(
        number_of_page=manager.dialog_data[f"{pagination_location}_pagination_current_page"]).encode('utf-8').
                          decode('unicode-escape'))


async def movie_overview_handler(callback: CallbackQuery, _, dialog_manager: DialogManager,
                                 *args, **kwargs) -> None:
    movie_tmdb_id = callback.data.split(':')[1]

    logging.info(f"Movie overview handler: {movie_tmdb_id}")

    dialog_manager.dialog_data["current_movie_tmdb_id"] = movie_tmdb_id

    await dialog_manager.switch_to(MovieDialogSG.movie_overview, show_mode=ShowMode.EDIT)
    await callback.answer("🎬 Movie overview")


async def get_movie_overview_data(dialog_manager: DialogManager, *args, **kwargs) -> dict:
    movie_tmdb_id = dialog_manager.dialog_data["current_movie_tmdb_id"]
    movie = await get_subject_overview_by_id(movie_tmdb_id, TypeOfSubject.movie)

    dialog_manager.dialog_data["current_movie_pretty_title"] = movie.pretty_title
    return movie.model_dump()


async def movie_suggestions_handler(callback: CallbackQuery, button: Button, dialog_manager: DialogManager,
                                    *args, **kwargs):
    logging.info("Movie suggestions handler")

    dialog_manager.dialog_data["pagination_location"] = PaginationLocation.suggestions.value
    dialog_manager.dialog_data["suggestions_pagination_current_page"] = 1

    dialog_manager.dialog_data["suggestions_depth_stack"].append(
        dialog_manager.dialog_data["current_movie_tmdb_id"])

    await dialog_manager.switch_to(MovieDialogSG.movie_suggestions, show_mode=ShowMode.EDIT)
    await callback.answer("🎬 Movie suggestions")


async def get_list_of_movie_suggestions(dialog_manager: DialogManager, *args, **kwargs) -> dict:
    current_movie_tmdb_id = dialog_manager.dialog_data["current_movie_tmdb_id"]

    movie_suggestions = await get_list_of_subject_suggestions_by_id(current_movie_tmdb_id, TypeOfSubject.movie)

    current_suggestions_base_movies_page = dialog_manager.dialog_data["suggestions_pagination_current_page"]

    total_number_of_pages = math.ceil(len(movie_suggestions) / ITEMS_PER_PAGE)

    dialog_manager.dialog_data["total_suggestions_pagination_pages"] = total_number_of_pages

    next_page_number, prev_page_number = await calculate_pagination(current_suggestions_base_movies_page,
                                                                    total_number_of_pages)

    return {
        "base_movies": movie_suggestions[(current_suggestions_base_movies_page - 1) * ITEMS_PER_PAGE:
                                         current_suggestions_base_movies_page * ITEMS_PER_PAGE],
        "next_page": navigation_emoji.format(number_of_page=next_page_number).encode('utf-8').decode('unicode-escape'),
        "prev_page": navigation_emoji.format(number_of_page=prev_page_number).encode('utf-8').decode('unicode-escape'),
        "current_page": current_suggestions_base_movies_page,
        "total_number_of_pages": total_number_of_pages
    }


async def go_to_previous_movie(callback: CallbackQuery, _, dialog_manager: DialogManager):
    await suggestions_previous_movie_handler(dialog_manager, TypeOfSubject.movie)
    await dialog_manager.switch_to(MovieDialogSG.movie_overview, show_mode=ShowMode.EDIT)
    await callback.answer("🎬 Movie overview")


async def go_to_previous_movie_suggestions(callback: CallbackQuery, _, dialog_manager: DialogManager):
    await previous_movie_suggestions_handler(dialog_manager, TypeOfSubject.movie)
    await dialog_manager.switch_to(MovieDialogSG.movie_suggestions, show_mode=ShowMode.EDIT)
    await callback.answer("🎬 Movie suggestions")
