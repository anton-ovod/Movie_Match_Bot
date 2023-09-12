from typing import List

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from filters.callback_factories import KeyboardMovieCallBackFactory, BackCallbackFactory, PageCallbackFactory, \
    MovieCallBackFactory
from models.movie import KeyboardMovie, Movie

keys_emojis = {
    1: "1️⃣",
    2: "2️⃣",
    3: "3️⃣",
    4: "4️⃣",
    5: "5️⃣",
    6: "6️⃣",
    7: "7️⃣",
    8: "8️⃣",
    9: "9️⃣",
    10: "🔟",
}


def get_page_of_movies_keyboard(movies: List[KeyboardMovie], page_number: int):
    movies_number = len(movies)
    movies_builder = InlineKeyboardBuilder()
    nav_builder = InlineKeyboardBuilder()
    if movies_number - (page_number * 10) >= 10:
        for movie in movies[(page_number - 1) * 10: page_number * 10]:
            movies_builder.button(text=movie.pretty_title,
                                  callback_data=KeyboardMovieCallBackFactory(title=movie.title,
                                                                             release_date=movie.release_date,
                                                                             tmdb_id=movie.tmdb_id))
        if page_number == 1:
            nav_builder.button(text=" ⬅️ Back", callback_data=BackCallbackFactory(to="search:movie"))
        else:
            nav_builder.button(text=f"f{keys_emojis[page_number - 1]}",
                               callback_data=PageCallbackFactory(type="movie", page=page_number - 1))

        nav_builder.button(text=" 🏠 Home", callback_data=BackCallbackFactory(to="home"))

        nav_builder.button(text=f"{keys_emojis[page_number + 1]}",
                           callback_data=PageCallbackFactory(type="movie", page=page_number + 1))

    elif 10 > movies_number - (page_number * 10) >= 0:
        for movie in movies[(page_number - 1) * 10:]:
            movies_builder.button(text=movie.pretty_title,
                                  callback_data=KeyboardMovieCallBackFactory(title=movie.title,
                                                                             release_date=movie.release_date,
                                                                             tmdb_id=movie.tmdb_id))
        if page_number == 1:
            nav_builder.button(text=" ⬅️ Back", callback_data=BackCallbackFactory(to="search:movie"))
        else:
            nav_builder.button(text=f"{keys_emojis[page_number - 1]}",
                               callback_data=PageCallbackFactory(type="movie", page=page_number - 1))

        nav_builder.button(text=" 🏠 Home", callback_data=BackCallbackFactory(to="home"))
        nav_builder.button(text=" 🚪 Close", callback_data=BackCallbackFactory(to="close"))

    movies_builder.adjust(1)
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
