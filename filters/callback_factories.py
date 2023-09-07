from aiogram.filters.callback_data import CallbackData


class BackCallbackFactory(CallbackData, prefix="back", sep="_"):
    to: str


class SearchCallbackFactory(CallbackData, prefix="search", sep="_"):
    type: str = None


class KeyboardMovieCallBackFactory(CallbackData, prefix="movie", sep="_"):
    tmdb_id: str


class MovieCallBackFactory(CallbackData, prefix="movie", sep=":"):
    feature: str


class PageCallbackFactory(CallbackData, prefix="page", sep=":"):
    type: str
    page: int
