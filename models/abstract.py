from abc import ABC, abstractmethod
from typing import Dict, List

from models.base import BaseSubject
from models.common import Provider, Actor, Rating


class AbstractDetailedSubject(BaseSubject, ABC):
    imdb_id: str | None = None
    poster_url: str | None = None
    trailer_url: str | None = None
    tagline: str | None = None

    homepage: str | None = None
    genres: List[str] | None = []
    overview: str | None = None
    cast: List[Actor] | None = []

    ratings: List[Rating] | None = []
    awards: str | None = None
    countries: List[str] | None = []
    age_categories: str | None = None

    rotten_tomatoes_url: str | None = None
    metacritic_url: str | None = None
    imdb_url: str | None = None
    tmdb_url: str | None = None

    providers_deep_link: str | None = None
    providers: Dict[str, List[Provider]] | None = {
        "buy": [],
        "rent": [],
        "flatrate": []
    }

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
        self._create_specific_links()

    @abstractmethod
    def _create_specific_links(self) -> None:
        pass
