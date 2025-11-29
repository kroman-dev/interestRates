from datetime import date
from abc import ABC, abstractmethod
from typing import List

from ir.scheduler.businessDayConvention.businessDayConvention import \
    BusinessDayConvention
from ir.scheduler.calendar.genericCalendar import GenericCalendar
from ir.scheduler.schedule.scheduleData import ScheduleData
from ir.scheduler.stubPeriod.genericStubPeriod import GenericStubPeriod


class GenericSchedule(ABC):

    def __init__(
            self,
            effectiveDate: date,
            terminationDate: date,
            frequency: str,
            businessDayConvention: BusinessDayConvention,
            endOfMonth: bool,
            stubPeriod: GenericStubPeriod,
            calendar: GenericCalendar,
            paymentLag: int = 0
    ):
        self._effectiveDate = effectiveDate
        self._terminationDate = terminationDate
        self._frequency = frequency
        self._businessDayConvention = businessDayConvention
        self._endOfMonth = endOfMonth
        self._stubPeriod = stubPeriod
        self._calendar = calendar
        self._schedule = self.createSchedule(
                effectiveDate=effectiveDate,
                terminationDate=terminationDate,
                frequency=frequency,
                businessDayConvention=businessDayConvention,
                endOfMonth=endOfMonth,
                stubPeriod=stubPeriod,
                calendar=calendar,
                paymentLag=paymentLag
        )

    def getSchedule(self) -> ScheduleData:
        return self._schedule

    @staticmethod
    def _adjustSchedule(
            unadjustedSchedule: List[date],
            calendar: GenericCalendar,
            businessDayConvention: BusinessDayConvention,
            endOfMonth: bool
    ) -> List[date]:
        effectiveDate = unadjustedSchedule[0]
        terminationDate = unadjustedSchedule[-1]
        schedule = []
        for unadjustedDate in unadjustedSchedule[:-1]:
            if endOfMonth and calendar.isLastMonthBusinessDay(effectiveDate):
                adjustedDate = calendar.getLastMonthBusinessDay(unadjustedDate)
            else:
                adjustedDate = businessDayConvention.adjust(
                    date=unadjustedDate,
                    calendar=calendar
                )

            schedule.append(adjustedDate)

        # termination date case
        if endOfMonth and calendar.isLastMonthBusinessDay(effectiveDate) \
                and (effectiveDate.day == terminationDate.day):
            schedule.append(
                businessDayConvention.adjust(
                    date=calendar.getLastMonthBusinessDay(
                        unadjustedSchedule[-1]
                    ),
                    calendar=calendar
                )
            )
        else:
            schedule.append(
                businessDayConvention.adjust(
                    date=unadjustedSchedule[-1],
                    calendar=calendar
                )
            )

        if (schedule[0] == schedule[-1]) and (len(schedule) != 1):
            raise ValueError("Schedule is not correct")

        return schedule

    @staticmethod
    @abstractmethod
    def createSchedule(
            effectiveDate: date,
            terminationDate: date,
            frequency: str,
            businessDayConvention: BusinessDayConvention,
            endOfMonth: bool,
            stubPeriod: GenericStubPeriod,
            calendar: GenericCalendar,
            paymentLag: int = 0
    ) -> ScheduleData:
        pass

    def __repr__(self):
        return self._schedule.__repr__()
