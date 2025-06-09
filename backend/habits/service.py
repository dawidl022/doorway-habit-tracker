from uuid import UUID, uuid4

from . import dtos
from .models import Habit
from .repository import HabitRepository


class HabitService:
    def __init__(self, repository: HabitRepository):
        self.repository = repository

    def get_all(self) -> list[Habit]:
        return self.repository.get_all()

    def get(self, id: UUID) -> Habit | None:
        return self.repository.get(id)

    def create(self, new_habit: dtos.NewHabit) -> dtos.CreatedHabit:
        habit_id = uuid4()
        self.repository.upsert(Habit(id=habit_id, description=new_habit.description))
        return dtos.CreatedHabit(habit_id)

    def update(self, id: UUID, new_habit: dtos.NewHabit):
        return self.repository.upsert(Habit(id=id, description=new_habit.description))

    def delete(self, id: UUID):
        return self.repository.delete(id)
