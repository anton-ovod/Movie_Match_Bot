from aiogram.filters.callback_data import CallbackData

from datetime import date


class BackCallbackFactory(CallbackData, prefix="back", sep="_"):
    to: str


class SearchCallbackFactory(CallbackData, prefix="search", sep="_"):
    type: str = None


class KeyboardMovieCallBackFactory(CallbackData, prefix="movie", sep="~"):
    tmdb_id: int


class MovieCallBackFactory(CallbackData, prefix="movie", sep=":"):
    feature: str


class PageCallbackFactory(CallbackData, prefix="page", sep=":"):
    type: str
    page: int
