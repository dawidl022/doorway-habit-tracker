from abc import ABC, abstractmethod
from uuid import UUID

import sqlalchemy
import sqlalchemy.orm
from config import DbConfig

from .models import Habit
from .tables import Base
from .tables import Habit as HabitTable


class HabitRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[Habit]:
        """Retrieve all habits."""
        pass

    @abstractmethod
    def get(self, id: UUID) -> Habit | None:
        """Retrieve a habit by its ID."""
        pass

    @abstractmethod
    def upsert(self, habit):
        """Create or update a habit."""
        pass

    @abstractmethod
    def delete(self, id: UUID):
        """Delete a habit by its ID."""
        pass


class InMemoryHabitRepository(HabitRepository):
    """Simple in-memory implementation of HabitRepository for testing
    purposes."""

    def __init__(self):
        self.habits = {}

    def get_all(self) -> list[Habit]:
        return list(self.habits.values())

    def get(self, id: UUID) -> Habit | None:
        return self.habits.get(id)

    def upsert(self, habit: Habit):
        self.habits[habit.id] = habit

    def delete(self, id: UUID):
        # TODO should cascade delete check-ins, as such a single in-memory
        # repository should contain both habits and check-ins
        if id in self.habits:
            del self.habits[id]


class SqlHabitRepository(HabitRepository):
    def __init__(self, Session: sqlalchemy.orm.sessionmaker[sqlalchemy.orm.Session]):
        self.Session = Session

    def get_all(self) -> list[Habit]:
        with self.Session() as session:
            query = sqlalchemy.select(HabitTable)
            result = session.scalars(query).all()

            return [
                Habit(id=habit.id, description=habit.description) for habit in result
            ]

    def get(self, id: UUID) -> Habit | None:
        with self.Session() as session:
            query = sqlalchemy.select(HabitTable).where(HabitTable.id == id)
            result = session.scalars(query).first()

            if result is None:
                return None

            return Habit(id=result.id, description=result.description)

    def upsert(self, habit: Habit):
        with self.Session() as session:
            habit_row = HabitTable(id=habit.id, description=habit.description)
            session.merge(habit_row)
            session.commit()

    def delete(self, id: UUID):
        with self.Session() as session:
            query = sqlalchemy.delete(HabitTable).where(HabitTable.id == id)
            session.execute(query)
            session.commit()
