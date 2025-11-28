from datetime import date
from typing import List

from ir.scheduler.businessDayConvention.businessDayConvention import \
    BusinessDayConvention
from ir.scheduler.calendar.genericCalendar import GenericCalendar
from ir.scheduler.period.period import Period
from ir.scheduler.stubPeriod.genericStubPeriod import GenericStubPeriod


class ShortBack(GenericStubPeriod):

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
        rawSchedule = [startDate]
        referenceDate = startDate
        while endDate > referenceDate:
            referenceDate += Period(frequency)

            if endDate > referenceDate:
                rawSchedule.append(referenceDate)

        rawSchedule.append(endDate)

        schedule = cls._adjustRawSchedule(
            rawSchedule=rawSchedule,
            calendar=calendar,
            businessDayConvention=businessDayConvention,
            endOfMonth=endOfMonth
        )

        return schedule
