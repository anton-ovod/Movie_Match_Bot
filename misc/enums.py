from enum import Enum


class TypeOfSubject(Enum):
    movie = "movie"
    tv_show = "tv"
    person = "person"


class PaginationDirection(Enum):
    next = 1
    previous = -1
