from datetime import date
from typing import List

from ir.scheduler.businessDayConvention.businessDayConvention import \
    BusinessDayConvention
from ir.scheduler.calendar.genericCalendar import GenericCalendar
from ir.scheduler.period.period import Period
from ir.scheduler.stubPeriod.genericStubPeriod import GenericStubPeriod


class ShortFront(GenericStubPeriod):

    @classmethod
    def makeSchedule(
            cls,
            startDate: date,
            endDate: date,
            frequency: str,
            calendar: GenericCalendar,
            businessDayConvention: BusinessDayConvention,
            endOfMonth: bool
    ) -> List[date]:
        rawSchedule = [endDate]
        referenceDate = endDate
        while referenceDate > startDate:
            referenceDate -= Period(frequency)

            if referenceDate > startDate:
                rawSchedule.append(referenceDate)

        rawSchedule.append(startDate)

        schedule = cls._adjustRawSchedule(
            rawSchedule=rawSchedule,
            calendar=calendar,
            businessDayConvention=businessDayConvention,
            endOfMonth=endOfMonth
        )

        return schedule[::-1]
