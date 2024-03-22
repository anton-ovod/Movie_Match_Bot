from pydantic import BaseModel, PositiveInt
from datetime import date


class BaseSubject(BaseModel):
    tmdb_id: PositiveInt = None
    pretty_title: str = None

    def __getitem__(self, item):
        return getattr(self, item)

    @property
    def json_data(self) -> str:
        return self.model_dump_json()


class BaseMovie(BaseSubject):
    title: str = None
    release_date: date | None = None


class BaseTVShow(BaseSubject):
    name: str = None
    first_air_date: date | None = None


class BasePerson(BaseSubject):
    name: str = None
    known_for_department: str = None
