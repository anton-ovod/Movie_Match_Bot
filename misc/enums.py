from enum import Enum
from misc.states import MovieDialogSG, TVShowDialogSG, PersonDialogSG, HomeDialogSG
from models.base import BaseMovie, BasePerson, BaseTVShow
from models.detailedmovie import DetailedMovie
from models.detailedperson import DetailedPerson
from models.detailedtvshow import DetailedTVShow


class SubjectsModels(Enum):
    MOVIE = (BaseMovie, DetailedMovie)
    TVSHOW = (BaseTVShow, DetailedTVShow)
    PERSON = (BasePerson, DetailedPerson)

    @classmethod
    def from_string(cls, value):
        for subject in cls:
            if value.lower() == subject.name.lower():
                return subject
        raise ValueError(f"No enum member with name '{value}'")

    @property
    def base_class(self):
        return self.value[0]

    @property
    def detailed_class(self):
        return self.value[1]


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
    TVSHOW = ("TV", TVShowDialogSG.TITLE_REQUEST, "📺")
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
    MAIN = "main"
    SUGGESTIONS = "suggestions"
