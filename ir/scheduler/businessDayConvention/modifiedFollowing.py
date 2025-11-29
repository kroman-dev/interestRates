from typing import TYPE_CHECKING

import datetime

from ir.scheduler.period.period import Period
from ir.scheduler.businessDayConvention.following import Following
from ir.scheduler.businessDayConvention.preceding import Preceding
from ir.scheduler.businessDayConvention.businessDayConvention \
    import BusinessDayConvention

if TYPE_CHECKING:
    from ir.scheduler.calendar.genericCalendar import GenericCalendar


class ModifiedFollowing(BusinessDayConvention):

    @staticmethod
    def adjust(
            date: datetime.date,
            calendar: 'GenericCalendar'
    ) -> datetime.date:
        adjustedDate = Following.adjust(
            date=date,
            calendar=calendar
        )
        if date.month != adjustedDate.month:
            return Preceding.adjust(
            date=date,
            calendar=calendar
        )

        return adjustedDate

