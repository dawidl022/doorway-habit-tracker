import datetime
from abc import ABC, abstractmethod
from uuid import UUID

import sqlalchemy.orm

from .models import CheckIn
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

    def habit_id_check_ins_by_date(self, date: datetime.date) -> list[UUID]:
        """List all habit IDs that have a check-in on a specific date."""
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
