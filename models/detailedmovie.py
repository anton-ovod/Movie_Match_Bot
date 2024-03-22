from pydantic import PositiveInt

from models.base import BaseMovie
from models.abstract import AbstractDetailedSubject

from config_reader import config


class DetailedMovie(BaseMovie, AbstractDetailedSubject):

    runtime: PositiveInt | None = None

    def _create_specific_links(self) -> None:
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
                    self.rotten_tomatoes_url = (f"{config.search_rot_url.get_secret_value()}/m/"
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
                    self.metacritic_url = (f"{config.search_meta_url.get_secret_value()}/m/"
                                           f"{title.lower()}")

    @property
    def json_data(self) -> str:
        self.calculate_average_rating()
        self.create_links()
        return self.model_dump_json()
