from abc import ABC, abstractmethod
from datetime import date
from typing import List

from ir.scheduler.businessDayConvention.businessDayConvention import \
    BusinessDayConvention
from ir.scheduler.calendar.genericCalendar import GenericCalendar
from ir.scheduler.period.period import Period


class GenericStubPeriod(ABC):

    @staticmethod
    @abstractmethod
    def makeSchedule(
            startDate: date,
            endDate: date,
            frequency: str,
            calendar: GenericCalendar,
            businessDayConvention: BusinessDayConvention,
            endOfMonth: bool
    ) -> List[date]:
        pass

    @staticmethod
    def _adjustRawSchedule(
            rawSchedule: List[date],
            calendar: GenericCalendar,
            businessDayConvention: BusinessDayConvention,
            endOfMonth: bool
    ):
        schedule = []
        for scheduleDate in rawSchedule:
            schedule.append(
                calendar.advance(
                    date=scheduleDate,
                    period=Period("0D"),
                    businessDayConvention=businessDayConvention,
                    endOfMonth=endOfMonth
                )
            )

        if (schedule[0] == schedule[-1]) and (len(schedule) != 1):
            raise ValueError("Schedule is not correct")

        return schedule
