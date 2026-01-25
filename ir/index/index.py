from abc import ABC

from ir.dayCounter.genericDayCounter import GenericDayCounter
from ir.scheduler.businessDayConvention.genericBusinessDayConvention import \
    GenericBusinessDayConvention
from ir.scheduler.calendar.genericCalendar import GenericCalendar


class Index(ABC):

    def __init__(
            self,
            name: str,
            currency: str,
            tenor: str,
            endOfMonth: bool,
            businessDayConvention: GenericBusinessDayConvention,
            dayCounter: GenericDayCounter,
            calendar: GenericCalendar
    ):
        self._name = name
        self._currency = currency
        self._tenor = tenor
        self._endOfMonth = endOfMonth
        self._businessDayConvention = businessDayConvention
        self._dayCounter = dayCounter
        self._calendar = calendar

    def getName(self):
        return self._name

    def getCurrency(self):
        return self._currency

    def getTenor(self):
        return self._tenor

    def getEndOfMonth(self):
        return self._endOfMonth

    def getBusinessDayConvention(self):
        return self._businessDayConvention

    def getDayCounter(self):
        return self._dayCounter

    def getCalendar(self):
        return self._calendar
