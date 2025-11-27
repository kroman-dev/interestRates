from abc import ABC, abstractmethod
from typing import List

import datetime

from ir.scheduler.businessDayConvention.businessDayConvention import \
    BusinessDayConvention
from ir.scheduler.period.period import Period


class GenericCalendar(ABC):

    def __init__(self, name: str):
        self._name = name
        self._holidays: List[datetime.date] = []

    def addHoliday(self, date: datetime.date) -> None:
        self._holidays.append(date)

    @abstractmethod
    def isBusinessDay(self, date: datetime.date) -> bool:
        pass

    @staticmethod
    def isEndOfMonth(date: datetime.date) -> bool:
        if date.month != (date + datetime.timedelta(days=1)).month:
            return True
        return False

    @staticmethod
    def getEndOfMonth(date: datetime.date) -> datetime.date:
        newDate = date
        while newDate.month == date.month:
            newDate += datetime.timedelta(days=1)
        return newDate - datetime.timedelta(days=1)

    @abstractmethod
    def advance(
            self,
            date: datetime.date,
            period: Period,
            businessDayConvention: BusinessDayConvention,
            endOfMonth: bool
    ):
        """

        :param date:
        :param period:
        :param businessDayConvention:
        :param endOfMonth:
            Where the start date of a period is on the final business day of
            a particular calendar month, the end date is on the final
            business day of the end month (not necessarily the corresponding
            date in the end month).
        Ref:
         [1] OpenGamma, Interest Rate Instruments and Market Conventions Guide
        """
        pass

    def __str__(self):
        return f'{self._name}Calendar'

    def __repr__(self):
        return self.__str__()
