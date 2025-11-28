from datetime import date

from ir.scheduler.businessDayConvention.businessDayConvention import \
    BusinessDayConvention
from ir.scheduler.calendar.genericCalendar import GenericCalendar
from ir.scheduler.period.period import Period
from ir.scheduler.schedule.genericSchedule import GenericSchedule
from ir.scheduler.schedule.scheduleData import ScheduleData
from ir.scheduler.stubPeriod.genericStubPeriod import GenericStubPeriod


class Schedule(GenericSchedule):

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
        super().__init__(
            effectiveDate=effectiveDate,
            terminationDate=terminationDate,
            frequency=frequency,
            businessDayConvention=businessDayConvention,
            endOfMonth=endOfMonth,
            stubPeriod=stubPeriod,
            calendar=calendar,
            paymentLag=paymentLag
        )

    @staticmethod
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
        schedule = stubPeriod.makeSchedule(
            startDate=effectiveDate,
            endDate=terminationDate,
            frequency=frequency,
            calendar=calendar,
            businessDayConvention=businessDayConvention,
            endOfMonth=endOfMonth
        )

        accrualStartDates = schedule[:-1]
        accrualEndDates = schedule[1:]

        paymentDate = [
            _date + Period(f"{paymentLag}D") for _date in accrualEndDates
        ]

        return ScheduleData(
            accrualStartDates=accrualStartDates,
            accrualEndDates=accrualEndDates,
            paymentDates=paymentDate
        )
