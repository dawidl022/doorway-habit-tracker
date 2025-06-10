import datetime
from uuid import UUID, uuid4

from check_ins.repository import CheckInRepository

from . import dtos
from .models import Habit
from .repository import HabitRepository


class HabitService:
    def __init__(
        self, repository: HabitRepository, check_in_repository: CheckInRepository
    ):
        self.repository = repository
        self.check_in_repository = check_in_repository

    def get_all(self) -> list[dtos.HabitWithSummary]:
        """Retrieve all habits with a summary of whether they were completed today."""
        todays_habit_ids = set(
            self.check_in_repository.habit_id_check_ins_by_date(datetime.date.today())
        )
        habits = self.repository.get_all()

        return [
            dtos.HabitWithSummary(
                id=habit.id,
                description=habit.description,
                completed_today=habit.id in todays_habit_ids,
            )
            for habit in habits
        ]

    def get(self, id: UUID) -> Habit | None:
        """Retrieve a habit by its ID."""
        return self.repository.get(id)

    def create(self, new_habit: dtos.NewHabit) -> dtos.CreatedHabit:
        """Create a new habit with an auto-generated unique ID."""
        habit_id = uuid4()
        self.repository.upsert(Habit(id=habit_id, description=new_habit.description))
        return dtos.CreatedHabit(habit_id)

    def update(self, id: UUID, new_habit: dtos.NewHabit):
        """Update an existing habit by its ID."""
        return self.repository.upsert(Habit(id=id, description=new_habit.description))

    def delete(self, id: UUID):
        """Delete a habit by its ID."""
        return self.repository.delete(id)
