from typing import List, Dict
from pydantic import BaseModel, PositiveInt
from datetime import date

from config_reader import config


class TVShow(BaseModel):

    @property
    def json_data(self) -> str:
        return self.model_dump_json()
