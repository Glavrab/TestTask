from typing import Type

from fastapi import HTTPException, status


class TestTaskError(Exception):
    pass


class ObjectNotFound(TestTaskError):
    pass


class Conflict(TestTaskError):
    pass


NOT_FOUND = HTTPException(status_code=status.HTTP_404_NOT_FOUND)

CONFLICT = HTTPException(status_code=status.HTTP_409_CONFLICT)

EXCEPTION_TO_API_ERROR_MAPPING: dict[Type[TestTaskError], HTTPException] = {
    ObjectNotFound: NOT_FOUND,
    Conflict: CONFLICT,
}
