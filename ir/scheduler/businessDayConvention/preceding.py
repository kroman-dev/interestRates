from typing import TYPE_CHECKING

import datetime

from ir.scheduler.period.period import Period
from ir.scheduler.businessDayConvention.businessDayConvention \
    import BusinessDayConvention

if TYPE_CHECKING:
    from ir.scheduler.calendar.genericCalendar import GenericCalendar


class Preceding(BusinessDayConvention):

    @staticmethod
    def adjust(
            date: datetime.date,
            calendar: 'GenericCalendar'
    ) -> datetime.date:
        adjustedDate = date
        while not calendar.isBusinessDay(adjustedDate):
            adjustedDate -= Period('1D')

        return adjustedDate
