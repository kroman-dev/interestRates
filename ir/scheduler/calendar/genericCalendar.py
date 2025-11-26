from abc import ABC, abstractmethod

import datetime

from ir.scheduler.businessDayConvention.businessDayConvention import \
    BusinessDayConvention
from ir.scheduler.period.period import Period


class GenericCalendar(ABC):

    def __init__(self, name: str):
        self._name = name

    @abstractmethod
    def isBusinessDay(self, date: datetime.date) -> bool:
        pass

    @abstractmethod
    def isEndOfMonth(self, date: datetime.date) -> bool:
        pass

    @abstractmethod
    def getEndOfMonth(self, date: datetime.date) -> datetime.date:
        pass

    @abstractmethod
    def advance(
            self,
            date: datetime.date,
            period: Period,
            businessDayConvention: BusinessDayConvention,
            endOfMonth: bool
    ):
        pass
