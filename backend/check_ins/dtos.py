from dataclasses import dataclass

from .models import CheckIn as CheckInModel


@dataclass
class CheckIn:
    date: str

    def __init__(self, check_in: CheckInModel):
        self.date = check_in.date.isoformat()
