from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from typing import List
from models.movie import KeyboardMovie

from filters.callback_factories import KeyboardMovieCallBackFactory, BackCallbackFactory, PageCallbackFactory


def get_first_page_movies_keyboard(movies: List[KeyboardMovie], movies_number: int) -> InlineKeyboardMarkup:
    movies_builder = InlineKeyboardBuilder()
    nav_builder = InlineKeyboardBuilder()
    if movies_number > 10:
        for movie in movies[:movies_number // 2]:
            movies_builder.button(text=movie.title,
                                  callback_data=KeyboardMovieCallBackFactory(tmdb_id=movie.get_main_data.get("tmdb_id")))

        nav_builder.button(text=" « Back", callback_data=BackCallbackFactory(to="search:movie"))
        nav_builder.button(text=" 🏠 Home", callback_data=BackCallbackFactory(to="home"))
        nav_builder.button(text=" 2️⃣ ", callback_data=PageCallbackFactory(type="movie", page=2))
        nav_builder.adjust(3)
    else:
        for movie in movies:
            movies_builder.button(text=movie.title,
                                  callback_data=KeyboardMovieCallBackFactory(tmdb_id=movie.get_main_data.get("tmdb_id")))

        nav_builder.button(text=" « Back", callback_data=BackCallbackFactory(to="search:movie"))
        nav_builder.button(text=" 🏠 Home", callback_data=BackCallbackFactory(to="home"))
        nav_builder.button(text="Close", callback_data=BackCallbackFactory(to="close"))

    movies_builder.adjust(1)
    nav_builder.adjust(3)
    movies_builder.attach(nav_builder)

    return movies_builder.as_markup()


def get_second_page_movies_keyboard(movies: List[KeyboardMovie], movies_number: int) -> InlineKeyboardMarkup:
    movies_builder = InlineKeyboardBuilder()
    for movie in movies[movies_number // 2:]:
        movies_builder.button(text=movie.title,
                              callback_data=KeyboardMovieCallBackFactory(tmdb_id=movie.get_main_data.get("tmdb_id")))
    movies_builder.adjust(1)

    nav_builder = InlineKeyboardBuilder()
    nav_builder.button(text=" 1️⃣ ", callback_data=PageCallbackFactory(type="movie", page=1))
    nav_builder.button(text=" 🏠 Home", callback_data=BackCallbackFactory(to="home"))
    nav_builder.button(text=" Close ", callback_data=BackCallbackFactory(to="close"))
    nav_builder.adjust(3)

    movies_builder.attach(nav_builder)
    return movies_builder.as_markup()


def get_movie_buttons(page: int) -> InlineKeyboardMarkup:
    movie_buttons = InlineKeyboardBuilder()
    movie_buttons.button(text=" « Back", callback_data=PageCallbackFactory(type="movie", page=page))

    return movie_buttons.as_markup()


def get_back_button() -> InlineKeyboardMarkup:
    back_button = InlineKeyboardBuilder()
    back_button.button(text=" « Back", callback_data=BackCallbackFactory(to="search:movie"))

    return back_button.as_markup()
