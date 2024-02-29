from typing import List, Dict
from pydantic import BaseModel, PositiveInt
from datetime import date

from config_reader import config


class TVShow(BaseModel):
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
