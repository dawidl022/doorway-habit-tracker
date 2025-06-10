from typing import TYPE_CHECKING
from uuid import UUID

import sqlalchemy
from db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from check_ins.tables import CheckIn


class Habit(Base):
    __tablename__ = "habits"

    id: Mapped[UUID] = mapped_column(sqlalchemy.Uuid(as_uuid=True), primary_key=True)
    description: Mapped[str]
    check_ins: Mapped[list["CheckIn"]] = relationship(
        back_populates="habit", cascade="all, delete-orphan"
    )
