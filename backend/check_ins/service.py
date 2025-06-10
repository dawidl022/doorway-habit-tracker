import datetime

from .models import CheckIn, Streak
from .repository import CheckInRepository


class CheckInService:
    def __init__(self, repository: CheckInRepository):
        self.repository = repository

    def get_check_ins(self, habit_id: str) -> list[CheckIn]:
        """
        Retrieves all check-ins for a given habit.
        """
        # TODO check that habit exists, otherwise return none that will 404
        return self.repository.list_for_habit(habit_id)

    def check_in(self, habit_id: str, check_in: CheckIn):
        """
        Records a check-in for a habit on a specific date.
        If the check-in already exists, the action is a noop.
        """
        # TODO check that habit exists, otherwise return none that will 404
        self.repository.upsert(habit_id, check_in)

    def delete_check_in(self, habit_id: str, date: datetime.date):
        """
        Deletes a check-in for a habit on a specific date.
        """
        # TODO check that habit exists, otherwise return none that will 404
        self.repository.delete(habit_id, date)

    def get_streaks(self, habit_id: str) -> list[Streak]:
        """
        Retrieves all streaks for a given habit.
        A streak is defined as a continuous sequence of check-ins
        lasting at least 1 day.
        """
        # TODO check that habit exists, otherwise return none that will 404
        # TODO
        return self.repository.calc_streaks(habit_id)
