"""This module contains all the states for the bot"""

from aiogram.filters.state import StatesGroup, State


class HomeDialogSG(StatesGroup):
    """States for the home dialog"""

    home = State()
    about = State()
    help = State()
    settings = State()
    search = State()
    cinema = State()
    discover = State()


class MovieDialogSG(StatesGroup):
    """States for the movie dialog"""

    title_request = State()
    movies_pagination = State()
    movie_overview = State()


class PersonDialogSG(StatesGroup):
    """States for the person dialog"""

    name_request = State()


class ShowDialogSG(StatesGroup):
    """States for the show dialog"""

    title_request = State()
