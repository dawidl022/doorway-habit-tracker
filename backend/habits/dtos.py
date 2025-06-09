from dataclasses import dataclass


@dataclass
class NewHabit:
    description: str

    @staticmethod
    def from_dict(data: dict) -> "NewHabit":
        # TODO validate description is not empty, otherwise exception that turns
        # into 400 Bad Request with user-friendly message
        return NewHabit(data.get("description", ""))
