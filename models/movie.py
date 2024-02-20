from typing import List
from pydantic import BaseModel, PositiveInt
from datetime import date

from config_reader import config


class KeyboardMovie(BaseModel):
    # Data is getting from tmdb api
    title: str = None
    release_date: date | None = None
    pretty_title: str = None
    tmdb_id: PositiveInt = None

    def __getitem__(self, item):
        return getattr(self, item)

    @property
    def json_data(self) -> str:
        return self.model_dump_json()


class Rating(BaseModel):
    source: str
    value: int | float | str


class Actor(BaseModel):
    name: str
    character: str
    profile_url: str = None


class Movie(KeyboardMovie):
    # Data is getting from tmdb api
    imdb_id: str | None = None
    tagline: str | None = None
    overview: str | None = None
    poster_url: str | None = None
    trailer_url: str | None = None
    homepage: str | None = None
    runtime: PositiveInt | None = None
    genres: List[str] | None = []

    # Data is getting from omdb api
    ratings: List[Rating] | None = []
    cast: List[Actor] | None = []
    awards: str | None = None
    age_categories: str | None = None
    countries: List[str] | None = []

    # Self made links
    rotten_tomatoes_url: str | None = None
    metacritic_url: str | None = None
    imdb_url: str | None = None
    tmdb_url: str | None = None

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

    @property
    def json_data(self) -> str:
        self.calculate_average_rating()
        self.create_links()
        return self.model_dump_json()
