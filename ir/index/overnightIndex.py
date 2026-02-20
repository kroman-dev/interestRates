from abc import ABC

from ir.dayCounter.genericDayCounter import GenericDayCounter
from ir.scheduler.businessDayConvention.genericBusinessDayConvention import \
    GenericBusinessDayConvention
from ir.scheduler.calendar.genericCalendar import GenericCalendar
from ir.index.index import Index


class OvernightIndex(Index, ABC):

    def __init__(
            self,
            name: str,
            currency: str,
            endOfMonth: bool,
            businessDayConvention: GenericBusinessDayConvention,
            dayCounter: GenericDayCounter,
            calendar: GenericCalendar
    ):
        super().__init__(
            name=name,
            currency=currency,
            tenor='1D',
            endOfMonth=endOfMonth,
            businessDayConvention=businessDayConvention,
            dayCounter=dayCounter,
            calendar=calendar
        )
