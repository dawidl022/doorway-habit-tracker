from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Habit(Base):
    __tablename__ = "habits"

    # TODO use UUID for id
    id: Mapped[str] = mapped_column(primary_key=True)
    description: Mapped[str]
