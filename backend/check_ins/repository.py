import datetime
from abc import ABC, abstractmethod
from uuid import UUID

import sqlalchemy.orm
from sqlalchemy import text

from .models import CheckIn, Streak
from .tables import CheckIn as CheckInTable


class CheckInRepository(ABC):
    @abstractmethod
    def list_for_habit(self, habit_id: UUID) -> list[CheckIn]:
        """List all check-ins for a specific habit."""
        pass

    @abstractmethod
    def upsert(self, habit_id: UUID, check_in: CheckIn):
        """Check-in for a habit on a specific date. This method is idempotent."""
        pass

    @abstractmethod
    def delete(self, habit_id: UUID, date: datetime.date):
        """Delete a check-in for a habit on a specific date."""
        pass

    @abstractmethod
    def habit_id_check_ins_by_date(self, date: datetime.date) -> list[UUID]:
        """List all habit IDs that have a check-in on a specific date."""
        pass

    @abstractmethod
    def calc_streaks(self, habit_id: UUID) -> list[Streak]:
        """Calculate streaks for a specific habit."""
        pass


class SqlCheckInRepository(CheckInRepository):
    def __init__(self, Session: sqlalchemy.orm.sessionmaker[sqlalchemy.orm.Session]):
        self.Session = Session

    def list_for_habit(self, habit_id: UUID) -> list[CheckIn]:
        with self.Session() as session:
            return list(
                session.query(CheckInTable)
                .filter(CheckInTable.habit_id == habit_id)
                .all()
            )

    def upsert(self, habit_id: UUID, check_in: CheckIn):
        with self.Session() as session:
            check_in_row = CheckInTable(habit_id=habit_id, date=check_in.date)
            session.merge(check_in_row)
            session.commit()

    def delete(self, habit_id: UUID, date: datetime.date):
        with self.Session() as session:
            session.query(CheckInTable).filter(
                CheckInTable.habit_id == habit_id, CheckInTable.date == date
            ).delete()
            session.commit()

    def habit_id_check_ins_by_date(self, date: datetime.date) -> list[UUID]:
        with self.Session() as session:
            return [
                row.habit_id
                for row in session.query(CheckInTable.habit_id)
                .filter(CheckInTable.date == date)
                .all()
            ]

    def calc_streaks(self, habit_id: UUID) -> list[Streak]:
        with self.Session() as session:
            query = text(
                """
                SELECT MIN(date) AS start_date, MAX(date) AS end_date FROM (
                    SELECT habit_id, date, (date - (SELECT MIN(date) FROM check_ins) + 1 - ROW_NUMBER() OVER ()) AS streak_id
                    FROM check_ins
                    WHERE habit_id = :habit_id
                    ORDER BY date
                )
                GROUP BY streak_id;
                """
            )

            result = session.execute(query, {"habit_id": habit_id}).fetchall()
            return [
                Streak(start_date=row.start_date, end_date=row.end_date)
                for row in result
            ]
