import datetime

from typing import Union
from dateutil.relativedelta import relativedelta


class Period:

    _availableTenors = ['D', 'W', 'M', 'Q', 'S', 'Y']

    def __init__(self, period: str):
        self._period = period
        self._timeDelta = self._getTimeDelta(period.upper())
    
    @classmethod
    def _getTimeDelta(cls, period: str) -> relativedelta:
        if period[-1] == 'D':
            return relativedelta(days=int(period[:-1]))
        elif period[-1] == 'W':
            return relativedelta(weeks=int(period[:-1]))
        elif period[-1] == 'M':
            return relativedelta(months=int(period[:-1]))
        elif period[-1] == 'Q':
            return relativedelta(months=3 * int(period[:-1]))
        elif period[-1] == 'S':
            return relativedelta(months=6 * int(period[:-1]))
        elif period[-1] == 'Y':
            return relativedelta(years=int(period[:-1]))
        else:
            raise ValueError(
                f"Incorrect period "
                f"-> period must be like {cls._availableTenors}"
            )

    def advance(self, date: datetime.date) -> datetime.date:
        return date + self._timeDelta

    def retreat(self, date: datetime.date) -> datetime.date:
        return date - self._timeDelta

    def __radd__(
            self,
            term: Union[datetime.date, 'Period']
    ) -> Union[datetime.date, 'Period']:
        if isinstance(term, (datetime.date, datetime.datetime)):
            return self.advance(term)
        if isinstance(term, Period):
            if self._period[-1] == term._period[-1]:
                return Period(
                    str(
                        int(term._period[:-1]) + int(self._period[:-1])
                    ) + self._period[-1]
                )
        return NotImplemented('incorrect operation')

    def __add__(
            self,
            term: Union[datetime.date, 'Period']
    ) -> Union[datetime.date, 'Period']:
        if isinstance(term, (datetime.date, datetime.datetime)):
            return self.advance(term)
        if isinstance(term, Period):
            if self._period[-1] == term._period[-1]:
                return Period(
                    str(
                        int(term._period[:-1]) + int(self._period[:-1])
                    ) + self._period[-1]
                )
        return NotImplemented('incorrect operation')

    def __rsub__(self, term: datetime.date) -> datetime.date:
        if isinstance(term, (datetime.date, datetime.datetime)):
            return self.retreat(term)
        return NotImplemented('incorrect operation')
