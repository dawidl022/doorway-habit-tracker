from http import HTTPStatus
from uuid import UUID

from flask import abort, make_response


def validate_uuid(uuid_string: str) -> UUID:
    try:
        return UUID(uuid_string)
    except ValueError:
        raise ValidationError("invalid UUID format")


class ValidationError(ValueError):
    """Custom exception for validation errors in DTOs."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def handle(self):
        return {"error": self.message}, HTTPStatus.BAD_REQUEST


class HabitNotFoundError(Exception):
    def handle(self):
        return {"error": "habit not found"}, HTTPStatus.NOT_FOUND
