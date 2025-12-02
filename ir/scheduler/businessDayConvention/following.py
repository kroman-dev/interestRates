from typing import TYPE_CHECKING

import datetime

from ir.scheduler.period.period import Period
from ir.scheduler.businessDayConvention.genericBusinessDayConvention \
    import GenericBusinessDayConvention

if TYPE_CHECKING:
    from ir.scheduler.calendar.genericCalendar import GenericCalendar


class Following(GenericBusinessDayConvention):

    @staticmethod
    def adjust(
            date: datetime.date,
            calendar: 'GenericCalendar'
    ) -> datetime.date:
        adjustedDate = date
        while not calendar.isBusinessDay(adjustedDate):
            adjustedDate += Period('1D')

        return adjustedDate
