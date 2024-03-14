"""This module contains all the states for the bot"""

from aiogram.filters.state import StatesGroup, State


class HomeDialogSG(StatesGroup):
    """States for the home dialog"""

    HOME = State()
    ABOUT = State()
    HELP = State()
    SETTINGS = State()
    SEARCH = State()
    CINEMA = State()
    DISCOVER = State()


class MovieDialogSG(StatesGroup):
    """States for the movie dialog"""

    TITLE_REQUEST = State()
    BASE_MOVIES_PAGINATION = State()
    MOVIE_OVERVIEW = State()
    MOVIE_SUGGESTIONS = State()
    MOVIE_AVAILABILITY = State()


class PersonDialogSG(StatesGroup):
    """States for the person dialog"""

    NAME_REQUEST = State()


class TVShowDialogSG(StatesGroup):
    """States for the tvshow dialog"""

    TITLE_REQUEST = State()
    BASE_TVSHOWS_PAGINATION = State()
