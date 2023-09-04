from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from filters.callback_factories import MovieCallBackFactory, BackCallbackFactory, PageCallbackFactory


def get_first_page_movies_keyboard(movies, movies_number) -> InlineKeyboardMarkup:
    movies_builder = InlineKeyboardBuilder()
    for movie in movies[:movies_number // 2]:
        movies_builder.button(text=movie.title, callback_data=MovieCallBackFactory(id=movie.tmdb_id))
    movies_builder.adjust(1)

    nav_builder = InlineKeyboardBuilder()
    nav_builder.button(text=" « Back", callback_data=BackCallbackFactory(to="search:movie"))
    nav_builder.button(text=" 🏠 Home", callback_data=BackCallbackFactory(to="home"))
    nav_builder.button(text=" 2️⃣ ", callback_data=PageCallbackFactory(type="movie", page=2))
    nav_builder.adjust(3)

    movies_builder.attach(nav_builder)
    return movies_builder.as_markup()


def get_second_page_movies_keyboard(movies, movies_number) -> InlineKeyboardMarkup:
    movies_builder = InlineKeyboardBuilder()
    for movie in movies[movies_number // 2:]:
        movies_builder.button(text=movie.title, callback_data=MovieCallBackFactory(id=movie.tmdb_id))
    movies_builder.adjust(1)

    nav_builder = InlineKeyboardBuilder()
    nav_builder.button(text=" 1️⃣ ", callback_data=PageCallbackFactory(type="movie", page=1))
    nav_builder.button(text=" 🏠 Home", callback_data=BackCallbackFactory(to="home"))
    nav_builder.button(text=" Close ", callback_data=BackCallbackFactory(to="close"))
    nav_builder.adjust(3)

    movies_builder.attach(nav_builder)
    return movies_builder.as_markup()

