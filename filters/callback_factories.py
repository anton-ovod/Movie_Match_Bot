from aiogram.filters.callback_data import CallbackData


class BackCallbackFactory(CallbackData, prefix="back", sep="_"):
    to: str


class SearchCallbackFactory(CallbackData, prefix="search", sep="_"):
    type: str = None


class MovieCallBackFactory(CallbackData, prefix="movie", sep="_"):
    id: str


class PageCallbackFactory(CallbackData, prefix="second_page", sep=":"):
    type: str
    page: int
