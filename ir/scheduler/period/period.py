import datetime

from dateutil.relativedelta import relativedelta


class Period:

    _availableTenors = ['D', 'W', 'M', 'Q', 'S', 'Y']

    def __init__(self, period: str):
        self._period = period.upper()
        self._timeDelta = self._getTimeDelta()

    def _getTimeDelta(self) -> relativedelta:
        if self._period[-1] == 'D':
            return relativedelta(days=int(self._period[:-1]))
        elif self._period[-1] == 'W':
            return relativedelta(weeks=int(self._period[:-1]))
        elif self._period[-1] == 'M':
            return relativedelta(months=int(self._period[:-1]))
        elif self._period[-1] == 'Q':
            return relativedelta(months=3 * int(self._period[:-1]))
        elif self._period[-1] == 'S':
            return relativedelta(months=6 * int(self._period[:-1]))
        elif self._period[-1] == 'Y':
            return relativedelta(years=int(self._period[:-1]))
        else:
            raise ValueError(
                f"Incorrect period "
                f"-> period must be like {self._availableTenors}"
            )

    def advance(self, date: datetime.date) -> datetime.date:
        return date + self._timeDelta

    def retreat(self, date: datetime.date) -> datetime.date:
        return date - self._timeDelta

    def __radd__(self, date: datetime.date) -> datetime.date:
        if isinstance(date, (datetime.date, datetime.datetime)):
            return self.advance(date)
        return NotImplemented('date must be datetime')

    def __add__(self, date: datetime.date) -> datetime.date:
        if isinstance(date, (datetime.date, datetime.datetime)):
            return self.advance(date)
        return NotImplemented

    def __rsub__(self, date: datetime.date) -> datetime.date:
        if isinstance(date, (datetime.date, datetime.datetime)):
            return self.retreat(date)
        return NotImplemented
