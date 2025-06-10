import datetime
from dataclasses import dataclass

from validation import ValidationError


@dataclass(frozen=True)
class CheckIn:
    date: datetime.date

    @staticmethod
    def from_dict(data: dict) -> "CheckIn":
        date_str = data.get("date")
        if not isinstance(date_str, str):
            raise ValidationError("date field must be a string")

        try:
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValidationError:
            raise ValidationError("date field must be in YYYY-MM-DD format")

        if date > datetime.date.today():
            raise ValidationError("date cannot be in the future")

        return CheckIn(date)


@dataclass(frozen=True)
class Streak:
    start_date: datetime.date
    end_date: datetime.date

    @property
    def days(self) -> int:
        return (self.end_date - self.start_date).days + 1
