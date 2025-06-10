from datetime import date
from uuid import UUID

import pytest
from check_ins.models import CheckIn, Streak
from check_ins.repository import CheckInRepository
from check_ins.service import CheckInService
from config import register_routes
from flask import Flask
from flask_injector import FlaskInjector
from habits.models import Habit
from habits.repository import HabitRepository
from habits.service import HabitService
from injector import Binder


@pytest.fixture()
def app():
    app = Flask(__name__)
    app.config.update({"TESTING": True})

    register_routes(app)

    FlaskInjector(app, modules=[configure_dependencies])

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def configure_dependencies(binder: Binder):
    store = RepositoryBackingStore()
    habit_repo = InMemoryHabitRepository(store)
    check_in_repo = InMemoryCheckInRepository(store)

    habit_service = HabitService(habit_repo, check_in_repo)
    check_in_service = CheckInService(check_in_repo, habit_repo)

    binder.bind(HabitService, to=habit_service)
    binder.bind(CheckInService, to=check_in_service)


class RepositoryBackingStore:
    """
    Backing store for the in-memory repository.
    """

    def __init__(self):
        self.habits: dict[UUID, Habit] = {}
        self.check_ins: dict[UUID, list[date]] = {}


class InMemoryHabitRepository(HabitRepository):
    """Simple in-memory implementation of HabitRepository for testing
    purposes."""

    def __init__(self, data: RepositoryBackingStore):
        self.data = data

    def get_all(self) -> list[Habit]:
        return list(self.data.habits.values())

    def get(self, id: UUID) -> Habit | None:
        return self.data.habits.get(id)

    def upsert(self, habit: Habit):
        self.data.habits[habit.id] = habit

    def delete(self, id: UUID):
        if id in self.data.habits:
            del self.data.habits[id]

        if id in self.data.check_ins:
            del self.data.check_ins[id]


class InMemoryCheckInRepository(CheckInRepository):
    """Simple in-memory implementation of CheckInRepository for testing
    purposes."""

    def __init__(self, data: RepositoryBackingStore):
        self.data = data

    def list_for_habit(self, habit_id: UUID) -> list[date]:
        return [CheckIn(date) for date in self.data.check_ins.get(habit_id, [])]

    def upsert(self, habit_id: UUID, check_in: CheckIn):
        if habit_id not in self.data.check_ins:
            self.data.check_ins[habit_id] = []
        if check_in.date not in self.data.check_ins[habit_id]:
            self.data.check_ins[habit_id].append(check_in.date)

    def delete(self, habit_id: UUID, check_in_date: date):
        if (
            habit_id in self.data.check_ins
            and check_in_date in self.data.check_ins[habit_id]
        ):
            self.data.check_ins[habit_id].remove(check_in_date)

    def habit_id_check_ins_by_date(self, check_in_date: date) -> list[UUID]:
        return [
            habit_id
            for habit_id, check_ins in self.data.check_ins.items()
            if check_in_date in check_ins
        ]

    def calc_streaks(self, habit_id: UUID) -> list[Streak]:
        """Calculate streaks for a specific habit."""
        raise NotImplementedError(
            "Streak calculation is not implemented in the in-memory repository."
        )
