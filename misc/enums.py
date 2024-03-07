from enum import Enum


class TypeOfSubject(Enum):
    movie = "movie"
    tv_show = "tv"
    person = "person"


class PaginationLocation(Enum):
    main = "main"
    suggestions = "suggestions"


class PaginationDirection(Enum):
    next = 1
    previous = -1
