from typing import List
from pydantic import BaseModel, PositiveInt
from datetime import date

from config_reader import config

rating_characters = {
    0: "🌑🌑🌑🌑🌑",
    0.5: "🌗🌑🌑🌑🌑",
    1: "🌕🌑🌑🌑🌑",
    1.5: "🌕🌗🌑🌑🌑",
    2: "🌕🌕🌑🌑🌑",
    2.5: "🌕🌕🌗🌑🌑",
    3: "🌕🌕🌕🌑🌑",
    3.5: "🌕🌕🌕🌗🌑",
    4: "🌕🌕🌕🌕🌑",
    4.5: "🌕🌕🌕🌕🌗",
    5: "🌕🌕🌕🌕🌕"
}


class KeyboardMovie(BaseModel):
    # Data is getting from tmdb api
    title: str = None
    release_date: date | None = None
    tmdb_id: PositiveInt = None

    @property
    def pretty_title(self) -> str:
        return self.title + f" ({self.release_date.year})" if self.release_date else self.title


class Rating(BaseModel):
    source: str
    value: int | float | str


class Actor(BaseModel):
    name: str
    character: str
    profile_url: str = None


class Movie(KeyboardMovie):
    # Data is getting from tmdb api
    imdb_id: str = None
    tagline: str = None
    overview: str = None
    poster_url: str = None
    trailer_url: str = None
    homepage: str = None
    runtime: PositiveInt = None
    genres: List[str] = []

    # Data is getting from omdb api
    ratings: List[Rating] = []
    cast: List[Actor] = []
    awards: str = None
    countries: List[str] = []

    # Self made links
    rotten_tomatoes_url: str = None
    metacritic_url: str = None
    imdb_url: str = None
    tmdb_url: str = None

    def calculate_average_rating(self) -> None:
        if len(self.ratings) == 1:
            self.ratings.append(Rating(source="Average Rating", value=self.ratings[0].value))
        elif len(self.ratings) > 1:
            average_rating: int = 0
            for rating in self.ratings:
                average_rating += (rating.value if rating.source != "IMDB" else rating.value * 10)
            average_rating = int(average_rating / len(self.ratings))
            self.ratings.append(Rating(source="Average Rating", value=average_rating))
        elif len(self.ratings) == 0:
            self.ratings.append(Rating(source="Average Rating", value="Haven't rated yet"))

    def create_links(self) -> None:
        if self.imdb_id:
            self.imdb_url = f"https://www.imdb.com/title/{self.imdb_id}"
        if self.tmdb_id:
            self.tmdb_url = f"https://www.themoviedb.org/movie/{self.tmdb_id}"
        if self.ratings:
            for rating in self.ratings:
                if rating.source == "Rotten Tomatoes":
                    replacement_dict = {
                        ' ': '_',
                        '_': '_',
                        ':': '_',
                        '-': '_',
                        "'": '',
                        ",": '_',
                        '.': '_',
                        '!': '',
                        '?': '',
                        '&': 'and',
                    }
                    table = str.maketrans(replacement_dict)
                    title = self.title.translate(table)
                    title = title.replace("__", "_")
                    self.rotten_tomatoes_url = (f"{config.search_rot_url.get_secret_value()}"
                                                f"{title.lower()}")
                elif rating.source == "Metacritic":
                    replacement_dict = {
                        ' ': '-',
                        ':': '-',
                        "'": '',
                        '.': '-',
                        ',': '-',
                        '!': '',
                        '?': '',
                        '&': '',
                    }
                    table = str.maketrans(replacement_dict)
                    title = self.title.translate(table)
                    title = title.replace("--", "-")
                    self.metacritic_url = (f"{config.search_meta_url.get_secret_value()}"
                                           f"{title.lower()}")
