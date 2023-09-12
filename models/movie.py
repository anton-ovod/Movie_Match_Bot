from typing import List
from pydantic import BaseModel, PositiveInt
from datetime import date


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
