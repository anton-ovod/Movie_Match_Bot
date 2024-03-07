from enum import Enum


class TypeOfSubject(Enum):
    movie = "movie"
    tv_show = "tv"
    person = "person"


class TypeOfSubjectFeature(Enum):
    base_subjects = "base_subjects"
    overview = "overview"
    suggestions = "suggestions"


class PaginationDirection(Enum):
    next = 1
    previous = -1

