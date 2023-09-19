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


def get_page_of_movies_keyboard(movies: List[KeyboardMovie], page_number: int,
                                type_of_feature: str = "main") -> InlineKeyboardMarkup:
    movies_number = len(movies)
    movies_builder = InlineKeyboardBuilder()
    nav_builder = InlineKeyboardBuilder()
    back_callback_query = "search:movie" if type_of_feature == "main" else "close"
    page_callback_feature = "main" if type_of_feature == "main" else "recommendations"
    keyboard_movie_feature = f"{type_of_feature}"

    if movies_number - (page_number * 10) >= 10:
        for movie in movies[(page_number - 1) * 10: page_number * 10]:
            movies_builder.button(text=movie.pretty_title,
                                  callback_data=KeyboardMovieCallBackFactory(tmdb_id=movie.tmdb_id, page=page_number,
                                                                             feature=keyboard_movie_feature))
        if page_number == 1:
            if type_of_feature == "main":
                nav_builder.button(text=" ⬅️ Back", callback_data=BackCallbackFactory(to=back_callback_query))
            elif type_of_feature == "recommendations":
                nav_builder.button(text=" 🚪 Close", callback_data=BackCallbackFactory(to=back_callback_query))

        else:
            nav_builder.button(text=f"f{keys_emojis[page_number - 1]}",
                               callback_data=PageCallbackFactory(type="movie", page=page_number - 1))

        if type_of_feature == "main":
            nav_builder.button(text=" 🏠 Home", callback_data=BackCallbackFactory(to="home"))

        nav_builder.button(text=f"{keys_emojis[page_number + 1]}",
                           callback_data=PageCallbackFactory(type="movie", page=page_number + 1,
                                                             feature=page_callback_feature))

    elif 10 > movies_number - (page_number * 10) >= 0:
        for movie in movies[(page_number - 1) * 10:]:
            movies_builder.button(text=movie.pretty_title,
                                  callback_data=KeyboardMovieCallBackFactory(tmdb_id=movie.tmdb_id, page=page_number,
                                                                             feature=keyboard_movie_feature))
        if page_number == 1:
            if type_of_feature == "main":
                nav_builder.button(text=" ⬅️ Back", callback_data=BackCallbackFactory(to=back_callback_query))
            elif type_of_feature == "recommendations":
                nav_builder.button(text=" 🚪 Close", callback_data=BackCallbackFactory(to=back_callback_query))

        else:
            nav_builder.button(text=f"{keys_emojis[page_number - 1]}",
                               callback_data=PageCallbackFactory(type="movie", page=page_number - 1,
                                                                 feature=page_callback_feature))

            if type_of_feature == "main":
                nav_builder.button(text=" 🏠 Home", callback_data=BackCallbackFactory(to="home"))
            nav_builder.button(text=" 🚪 Close", callback_data=BackCallbackFactory(to="close"))
    else:
        for movie in movies[(page_number - 1) * 10:]:
            movies_builder.button(text=movie.pretty_title,
                                  callback_data=KeyboardMovieCallBackFactory(tmdb_id=movie.tmdb_id, page=page_number,
                                                                             feature=keyboard_movie_feature))
        if type_of_feature == "main":
            nav_builder.button(text=" ⬅️ Back", callback_data=BackCallbackFactory(to=back_callback_query))
            nav_builder.button(text=" 🏠 Home", callback_data=BackCallbackFactory(to="home"))

        nav_builder.button(text=" 🚪 Close", callback_data=BackCallbackFactory(to="close"))

    movies_builder.adjust(1)
    nav_builder.adjust(3)
    movies_builder.attach(nav_builder)

    return movies_builder.as_markup()


def get_movie_buttons(page: int, movie_data: Movie, type_of_feature: str = "main") -> InlineKeyboardMarkup:
    movie_buttons = InlineKeyboardBuilder()
    feature_callback_query = f"{type_of_feature}"

    if movie_data.homepage:
        movie_buttons.button(text="🏠 Homepage", url=movie_data.homepage)
    elif movie_data.imdb_url:
        movie_buttons.button(text="🏠 Homepage", url=movie_data.imdb_url)
    else:
        movie_buttons.button(text="🏠 Homepage", url=movie_data.tmdb_url)

    if movie_data.trailer_url:
        movie_buttons.button(text="🎞 Trailer", url=movie_data.trailer_url)

    if type_of_feature == "main":
        movie_buttons.button(text="🗂 Suggestions", callback_data=MovieCallBackFactory(feature="recommendations",
                                                                                      tmdb_id=movie_data.tmdb_id))
    else:
        movie_buttons.button(text="🌄 Poster", url=movie_data.poster_url)

    movie_buttons.button(text="📽 Availability", callback_data=MovieCallBackFactory(feature="availability",
                                                                                   tmdb_id=movie_data.tmdb_id))
    movie_buttons.button(text="⬅️ Back", callback_data=PageCallbackFactory(type="movie", page=page,
                                                                           feature=feature_callback_query))
    movie_buttons.button(text="🤲 Share", callback_data=MovieCallBackFactory(feature="share",
                                                                            tmdb_id=movie_data.tmdb_id))
    movie_buttons.adjust(2)
    return movie_buttons.as_markup()


def get_back_button(type_of_feature: str = "main") -> InlineKeyboardMarkup:
    back_button = InlineKeyboardBuilder()
    back_callback_query = "search:movie" if type_of_feature == "main" else "close"
    back_button.button(text=" ⬅️ Back", callback_data=BackCallbackFactory(to=back_callback_query))

    return back_button.as_markup()
