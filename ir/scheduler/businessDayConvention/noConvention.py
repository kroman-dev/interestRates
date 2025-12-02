from typing import TYPE_CHECKING

import datetime

from ir.scheduler.businessDayConvention.businessDayConvention \
    import BusinessDayConvention

if TYPE_CHECKING:
    from ir.scheduler.calendar.genericCalendar import GenericCalendar


class NoConvention(BusinessDayConvention):

    @staticmethod
    def adjust(
            date: datetime.date,
            calendar: 'GenericCalendar'
    ) -> datetime.date:
        return date
