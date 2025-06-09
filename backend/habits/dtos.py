from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class NewHabit:
    description: str

    @staticmethod
    def from_dict(data: dict) -> "NewHabit":
        description = data.get("description", "")

        if not isinstance(description, str):
            raise ValidationError("description field must be a string")

        description = description.strip()
        if len(description) == 0:
            raise ValidationError("description field cannot be empty")

        return NewHabit(description)


@dataclass(frozen=True)
class CreatedHabit:
    id: UUID

    def to_dict(self) -> dict:
        return {
            "id": self.id,
        }


class ValidationError(Exception):
    """Custom exception for validation errors in DTOs."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
