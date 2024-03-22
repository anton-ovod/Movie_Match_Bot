from pydantic import BaseModel


class Rating(BaseModel):
    source: str
    value: int | float | str


class Actor(BaseModel):
    name: str
    character: str
    profile_url: str = None


class Provider(BaseModel):
    provider_name: str
    provider_logo_url: str
