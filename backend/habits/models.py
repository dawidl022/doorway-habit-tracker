from dataclasses import dataclass


@dataclass(frozen=True)
class Habit:
    id: str
    description: str
