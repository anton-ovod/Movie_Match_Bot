from typing import List, Dict
from pydantic import PositiveInt
from datetime import date

from config_reader import config
from models.abstract import AbstractDetailedSubject
from models.base import BaseTVShow
from models.common import Actor


class DetailedTVShow(BaseTVShow, AbstractDetailedSubject):
    created_by: Actor | None = None
    last_air_date: date | None = None
    number_of_episodes: PositiveInt | None = None
    number_of_seasons: PositiveInt | None = None

    def _create_specific_links(self) -> None:
        if self.tmdb_id:
            self.tmdb_url = f"https://www.themoviedb.org/tv/{self.tmdb_id}"
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
                    title = self.name.translate(table)
                    title = title.replace("__", "_")
                    self.rotten_tomatoes_url = (f"{config.search_rot_url.get_secret_value()}/tv/"
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
                    title = self.name.translate(table)
                    title = title.replace("--", "-")
                    self.metacritic_url = (f"{config.search_meta_url.get_secret_value()}/tv/"
                                           f"{title.lower()}")

    @property
    def json_data(self) -> str:
        return self.model_dump_json()
