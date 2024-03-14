from typing import List, Dict
from pydantic import BaseModel, PositiveInt
from datetime import date

from config_reader import config


class Person(BaseModel):
    # Data is getting from tmdb api
    name: str = None
    birthday: date | None = None
    pretty_name: str = None
    tmdb_id: PositiveInt = None

    @property
    def json_data(self) -> str:
        return self.model_dump_json()
