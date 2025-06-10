from dataclasses import dataclass

from .models import CheckIn as CheckInModel


@dataclass
class CheckIn:
    date: str

    def __init__(self, check_in: CheckInModel):
        self.date = check_in.date.isoformat()


@dataclass
class Streak:
    start_date: str
    end_date: str
    days: input

    def __init__(self, streak: CheckInModel):
        self.start_date = streak.start_date.isoformat()
        self.end_date = streak.end_date.isoformat()
        self.days = (streak.end_date - streak.start_date).days + 1
