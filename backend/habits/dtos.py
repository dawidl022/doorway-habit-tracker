from dataclasses import dataclass
from uuid import UUID

from validation import ValidationError


@dataclass(frozen=True)
class NewHabit:
    description: str

    @staticmethod
    def from_dict(data: dict) -> "NewHabit":
        """Create a NewHabit instance from a dictionary, validating the input."""
        description = data.get("description")

        if not isinstance(description, str):
            raise ValidationError("description field must be a string")

        description = description.strip()
        if len(description) == 0:
            raise ValidationError("description field cannot be empty")

        return NewHabit(description)


@dataclass(frozen=True)
class CreatedHabit:
    id: UUID


@dataclass(frozen=True)
class HabitWithSummary:
    id: UUID
    description: str
    completed_today: bool

    def to_dict(self) -> dict:
        """Convert the habit to a camelCase dictionary representation, to return
        from the API."""
        return {
            "id": str(self.id),
            "description": self.description,
            "completedToday": self.completed_today,
        }
