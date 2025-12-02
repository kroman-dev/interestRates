from typing import TYPE_CHECKING

import datetime

from ir.scheduler.businessDayConvention.genericBusinessDayConvention \
    import GenericBusinessDayConvention

if TYPE_CHECKING:
    from ir.scheduler.calendar.genericCalendar import GenericCalendar


class NoConventionGeneric(GenericBusinessDayConvention):

    @staticmethod
    def adjust(
            date: datetime.date,
            calendar: 'GenericCalendar'
    ) -> datetime.date:
        return date
