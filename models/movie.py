from typing import List
from pydantic import BaseModel, PositiveInt, HttpUrl
from datetime import date

# from utils.imdb_api import get_movie_details_tmdb


class KeyboardMovie(BaseModel):
    # Data is getting from tmdb api
    title: str
    release_date: date | None
    tmdb_id: PositiveInt

    @property
    def pretty_title(self) -> str:
        return self.title + f" ({self.release_date.year})" if self.release_date else self.title


class Rating(BaseModel):
    source: str
    value: int


class Actor(BaseModel):
    name: str
    character: str
    profile_url: HttpUrl | None


class Movie(KeyboardMovie):
    # Data is getting from tmdb api
    imdb_id: PositiveInt | None = None
    tagline: str | None = None
    overview: str | None = None
    poster_url: HttpUrl | None = None
    trailer_url: HttpUrl | None = None
    homepage: HttpUrl | None = None
    runtime: PositiveInt | None = None
    genres: List[str] | None = None

    # Data is getting from omdb api
    ratings: List[Rating] | None = None
    cast: List[Actor] | None = None
    awards: str | None = None
    countries: List[str] | None = None

    # Self made links
    rotten_tomatoes_url: HttpUrl | None = None
    metacritic_url: HttpUrl | None = None
    imdb_url: HttpUrl | None = None
    tmdb_url: HttpUrl | None = None

    #async def fill_data(self) -> None:
        #await get_movie_details_tmdb(self)

    def _create_html_movie_ratings(self) -> str:
        star_characters = {
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
        average_rating = self._calculate_average_rating()
        try:
            star_rating = star_characters[round((average_rating / 20) * 2) / 2]
        except (TypeError, KeyError):
            star_rating = star_characters[0]

        return ""
