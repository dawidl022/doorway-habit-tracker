from uuid import UUID

import sqlalchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Habit(Base):
    __tablename__ = "habits"

    id: Mapped[UUID] = mapped_column(sqlalchemy.Uuid(as_uuid=True), primary_key=True)
    description: Mapped[str]
