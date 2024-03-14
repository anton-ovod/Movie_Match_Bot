from enum import Enum
from misc.states import MovieDialogSG, TVShowDialogSG, PersonDialogSG, HomeDialogSG
from models.movie import Movie
from models.person import Person
from models.tvshow import TVShow


class SubjectsModels(Enum):
    MOVIE = Movie
    TVSHOW = TVShow
    PERSON = Person


class StatesGroups(Enum):
    HOME = HomeDialogSG
    MOVIE = MovieDialogSG
    TVSHOW = TVShowDialogSG
    PERSON = PersonDialogSG


class HomeDialogOptions(Enum):
    HELP = ("Help", HomeDialogSG.HELP, "❓")
    ABOUT = ("About", HomeDialogSG.ABOUT, "📚")
    SEARCH = ("Search", HomeDialogSG.SEARCH, "🔍")
    CINEMA = ("Cinema", HomeDialogSG.CINEMA, "🍿")
    DISCOVER = ("Discover", HomeDialogSG.DISCOVER, "🌟")
    SETTINGS = ("Settings", HomeDialogSG.SETTINGS, "⚙️")

    @property
    def title(self):
        return self.value[0]

    @property
    def state(self):
        return self.value[1]

    @property
    def emoji(self):
        return self.value[2]


class SearchDialogOptions(Enum):
    MOVIE = ("Movie", MovieDialogSG.TITLE_REQUEST, "🎬")
    TVSHOW = ("Show", TVShowDialogSG.TITLE_REQUEST, "📺")
    PERSON = ("Person", PersonDialogSG.NAME_REQUEST, "👤")

    @property
    def title(self):
        return self.value[0]

    @property
    def state(self):
        return self.value[1]

    @property
    def emoji(self):
        return self.value[2]


class PaginationLocation(Enum):
    main = "main"
    suggestions = "suggestions"
