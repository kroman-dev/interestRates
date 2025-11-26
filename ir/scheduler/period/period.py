import datetime


class Period:

    def __init__(self, period: str):
        self._period = period

    def advance(self, date: datetime.date) -> datetime.date:
        pass
