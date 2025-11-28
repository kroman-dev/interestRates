from datetime import date
from abc import ABC, abstractmethod

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
