from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class Habit:
    id: UUID
    description: str
