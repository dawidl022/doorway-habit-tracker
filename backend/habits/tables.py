from uuid import UUID

import sqlalchemy
from db import Base
from sqlalchemy.orm import Mapped, mapped_column


class Habit(Base):
    __tablename__ = "habits"

    id: Mapped[UUID] = mapped_column(sqlalchemy.Uuid(as_uuid=True), primary_key=True)
    description: Mapped[str]
