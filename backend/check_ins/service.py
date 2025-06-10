import datetime
from uuid import UUID

from habits.repository import HabitRepository
from validation import HabitNotFoundError

from .models import CheckIn, Streak
from .repository import CheckInRepository


class CheckInService:
    def __init__(self, check_in_repo: CheckInRepository, habit_repo: HabitRepository):
        self.check_in_repo = check_in_repo
        self.habit_repo = habit_repo

    def get_check_ins(self, habit_id: UUID) -> list[CheckIn]:
        """
        Retrieves all check-ins for a given habit.
        """
        self._check_habit_exists(habit_id)
        return self.check_in_repo.list_for_habit(habit_id)

    def check_in(self, habit_id: UUID, check_in: CheckIn):
        """
        Records a check-in for a habit on a specific date.
        If the check-in already exists, the action is a noop.
        """
        self._check_habit_exists(habit_id)
        self.check_in_repo.upsert(habit_id, check_in)

    def delete_check_in(self, habit_id: UUID, date: datetime.date):
        """
        Deletes a check-in for a habit on a specific date.
        """
        self._check_habit_exists(habit_id)
        self.check_in_repo.delete(habit_id, date)

    def get_streaks(self, habit_id: UUID) -> list[Streak]:
        """
        Retrieves all streaks for a given habit.
        A streak is defined as a continuous sequence of check-ins
        lasting at least 1 day.
        """
        self._check_habit_exists(habit_id)
        return self.check_in_repo.calc_streaks(habit_id)

    def _check_habit_exists(self, habit_id: UUID):
        """
        Checks if a habit exists in the repository.
        Raises an exception if the habit does not exist.
        """
        if self.habit_repo.get(habit_id) is None:
            raise HabitNotFoundError()
