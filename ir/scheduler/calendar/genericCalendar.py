import datetime
from abc import ABC, abstractmethod
from typing import List

from ir.scheduler.businessDayConvention.genericBusinessDayConvention import \
    GenericBusinessDayConvention
from ir.scheduler.businessDayConvention.modifiedFollowing import \
    ModifiedFollowing
from ir.scheduler.period.period import Period


class GenericCalendar(ABC):

    def __init__(self, name: str):
        self._name = name
        self._holidays: List[datetime.date] = []

    def getLastMonthBusinessDay(
            self,
            date: datetime.date
    ) -> datetime.date:
        return ModifiedFollowing.adjust(
            date=self.getEndOfMonth(date),
            calendar=self
        )

    def isLastMonthBusinessDay(self, date: datetime.date) -> bool:
        if not self.isBusinessDay(date):
            return False
        if self.isBusinessDay(date + Period('1D')) \
                and ((date + Period('1D')).month == date.month):
            return False
        if self.isBusinessDay(date) and self.isEndOfMonth(date):
            return True
        if ModifiedFollowing.adjust(
                date=date + Period('1D'),
                calendar=self
        ) == date:
            return True

        return False

    def addHoliday(self, date: datetime.date) -> None:
        self._holidays.append(date)

    @abstractmethod
    def isBusinessDay(self, date: datetime.date) -> bool:
        pass

    @staticmethod
    def isEndOfMonth(date: datetime.date) -> bool:
        if date.month != (date + Period('1D')).month:
            return True
        return False

    @staticmethod
    def getEndOfMonth(date: datetime.date) -> datetime.date:
        newDate = date
        while newDate.month == date.month:
            newDate += Period('1D')
        return newDate - Period('1D')

    def advance(
            self,
            date: datetime.date,
            period: Period,
            businessDayConvention: GenericBusinessDayConvention,
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
        # TODO think about eom and following case:
            # https://quant.stackexchange.com/questions/73827/is-end-of-month-eom-rule-overrides-convention-rule-in-quantlib-schedule
            # https://quant.stackexchange.com/questions/78641/is-end-of-month-eom-rule-overrides-unadjusted-convention-rule-in-quantlib
        Ref:
         [1] OpenGamma, Interest Rate Instruments and Market Conventions Guide
        """
        if endOfMonth and self.isLastMonthBusinessDay(date):
            return self.getLastMonthBusinessDay(date + period)

        result = businessDayConvention.adjust(
            date=date + period,
            calendar=self
        )

        return result

    def retreat(
            self,
            date: datetime.date,
            period: Period,
            businessDayConvention: GenericBusinessDayConvention,
            endOfMonth: bool
    ):
        if endOfMonth and self.isLastMonthBusinessDay(date):
            return self.getLastMonthBusinessDay(date - period)

        result = businessDayConvention.adjust(
            date=date - period,
            calendar=self
        )

        return result

    def __str__(self):
        return f'{self._name}Calendar'

    def __repr__(self):
        return self.__str__()
