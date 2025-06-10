import datetime
from uuid import UUID

import sqlalchemy
from db import Base
from habits.tables import Habit
from sqlalchemy.orm import Mapped, mapped_column, relationship


class CheckIn(Base):
    __tablename__ = "check_ins"

    habit_id: Mapped[UUID] = mapped_column(
        sqlalchemy.ForeignKey("habits.id"), primary_key=True
    )
    # TODO remove unused field
    habit: Mapped[Habit] = relationship(back_populates="check_ins")
    date: Mapped[datetime.date] = mapped_column(sqlalchemy.Date, primary_key=True)
