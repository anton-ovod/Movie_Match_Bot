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

        # message = ""
        #
        # if self.poster_url:
        #     message += f"<a href='{self.poster_url}'><b>{self.pretty_title}</b></a>\n"
        # elif self.imdb_url:
        #     message += f"<a href='{self.imdb_url}'><b>{self.pretty_title}</b></a>\n"
        # else:
        #     message += f"<a href='{self.tmdb_url}'><b>{self.pretty_title}</b></a>\n"
        # if self.tagline:
        #     message += f"<i>{self.tagline}</i>\n"
        #
        # message += "\n"
        #
        # if self.genres:
        #     for genre in self.genres:
        #         message += f"#{genre.replace(' ', '')} "
        #     message += "\n"
        # if self.overview:
        #     message += f"{self.overview}\n"
        #
        # message += "\n"
        #
        # if ratings := self.ratings:
        #     if len(ratings) == 1:
        #         message += f"Average rating: <b>{ratings[0].value}</b>\n"
        #     else:
        #         average_star_rating = round((ratings[-1].value / 20) * 2) / 2
        #         message += f"<b>Average rating: {rating_characters[average_star_rating]} • {ratings[-1].value}</b>\n"
        #         for rating in ratings[:-1]:
        #             if rating.source == "TMDb":
        #                 message += f"<a href='{self.tmdb_url}'>TMDb</a>: {rating.value}\n"
        #             if rating.source == "IMDB":
        #                 message += f"<a href='{self.imdb_url}'>IMDb</a>: {rating.value}\n"
        #             if rating.source == "Rotten Tomatoes":
        #                 message += f"<a href='{self.rotten_tomatoes_url}'>Rotten Tomatoes</a>: {rating.value}\n"
        #             if rating.source == "Metacritic":
        #                 message += f"<a href='{self.metacritic_url}'>Metacritic</a>: {rating.value}\n"
        #
        # message += "\n"
        #
        # if self.awards:
        #     message += f"<b>Awards:</b> {self.awards}.\n\n"
        # if self.cast:
        #     message += f"<b>Director:</b> <a href='{self.cast[-1].profile_url}'>{self.cast[-1].name}</a>\n\n"
        # if self.cast[:-1]:
        #     message += "<b>Actors:</b>\n"
        #     for actor in self.cast[:-1]:
        #         message += f"<a href='{actor.profile_url}'><i>{actor.name}</i></a> as {actor.character}\n"
        #
        # bottom_line = ""
        # if self.age_categories:
        #     bottom_line += f"{self.age_categories}"
        #     bottom_line += " | "
        # if self.runtime:
        #     bottom_line += f"{self.runtime} min"
        # if self.countries:
        #     bottom_line += " | " if self.runtime else ""
        #     bottom_line += f"{', '.join(self.countries)}"
        #
        # message += f"\n{bottom_line}"
        #
        # return message
