from typing import List

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from filters.callback_factories import KeyboardMovieCallBackFactory, BackCallbackFactory, PageCallbackFactory, MovieCallBackFactory
from models.movie import KeyboardMovie, Movie


def get_first_page_movies_keyboard(movies: List[KeyboardMovie], movies_number: int) -> InlineKeyboardMarkup:
    movies_builder = InlineKeyboardBuilder()
    nav_builder = InlineKeyboardBuilder()
    if movies_number > 10:
        for movie in movies[:movies_number // 2]:
            movies_builder.button(text=movie.title,
                                  callback_data=KeyboardMovieCallBackFactory(
                                      tmdb_id=movie.get_main_data.get("tmdb_id")))

        nav_builder.button(text=" ⬅️ Back", callback_data=BackCallbackFactory(to="search:movie"))
        nav_builder.button(text=" 🏠 Home", callback_data=BackCallbackFactory(to="home"))
        nav_builder.button(text=" 2️⃣ ", callback_data=PageCallbackFactory(type="movie", page=2))
        nav_builder.adjust(3)
    else:
        for movie in movies:
            movies_builder.button(text=movie.title,
                                  callback_data=KeyboardMovieCallBackFactory(
                                      tmdb_id=movie.get_main_data.get("tmdb_id")))

        nav_builder.button(text=" ⬅️ Back", callback_data=BackCallbackFactory(to="search:movie"))
        nav_builder.button(text=" 🏠 Home", callback_data=BackCallbackFactory(to="home"))
        nav_builder.button(text=" 🚪 Close", callback_data=BackCallbackFactory(to="close"))

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
    nav_builder.button(text=" 🚪 Close ", callback_data=BackCallbackFactory(to="close"))
    nav_builder.adjust(3)

    movies_builder.attach(nav_builder)
    return movies_builder.as_markup()


def get_movie_buttons(page: int, movie_data: Movie) -> InlineKeyboardMarkup:
    movie_buttons = InlineKeyboardBuilder()
    if movie_data.homepage:
        movie_buttons.button(text=" 🏠 Homepage", url=movie_data.homepage)
    elif movie_data.imdb_url:
        movie_buttons.button(text=" 🏠 Homepage", url=movie_data.imdb_url)
    elif movie_data.tmdb_url:
        movie_buttons.button(text=" 🏠 Homepage", url=movie_data.tmdb_url)
    else:
        movie_buttons.button(text=" 🌄 Poster", url=movie_data.poster_url)

    if movie_data.trailer_url:
        movie_buttons.button(text=" 🎞 Trailer", url=movie_data.trailer_url)
    else:
        movie_buttons.button(text=" 🎞 Trailer",
                             url="https://www.youtube.com/results?search_query=trailer " + movie_data.title_year)

    movie_buttons.button(text=" 🗂 Recommendations", callback_data=MovieCallBackFactory(feature="recommendations"))
    movie_buttons.button(text=" 📼 Where to watch", callback_data=MovieCallBackFactory(feature="watch"))
    movie_buttons.button(text=" ⬅️ Back", callback_data=PageCallbackFactory(type="movie", page=page))
    movie_buttons.button(text=" 🤲 Share", switch_inline_query=movie_data.title_year)
    movie_buttons.adjust(2)
    return movie_buttons.as_markup()


def get_back_button() -> InlineKeyboardMarkup:
    back_button = InlineKeyboardBuilder()
    back_button.button(text=" ⬅️ Back", callback_data=BackCallbackFactory(to="search:movie"))

    return back_button.as_markup()
