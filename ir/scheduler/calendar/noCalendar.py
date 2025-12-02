import datetime

from ir.scheduler.businessDayConvention.businessDayConvention import \
    BusinessDayConvention
from ir.scheduler.calendar.genericCalendar import GenericCalendar
from ir.scheduler.period.period import Period


class NoCalendar(GenericCalendar):

    def __init__(self):
        super().__init__(name='NoCalendar')

    def isBusinessDay(self, date: datetime.date) -> bool:
        if date.weekday() == 6 or date.weekday() == 7:
            return False
        return True

    def advance(
            self,
            date: datetime.date,
            period: Period,
            businessDayConvention: BusinessDayConvention,
            endOfMonth: bool
    ):
        if endOfMonth and self.isLastMonthBusinessDay(date):
            return self.getLastMonthBusinessDay(date + period)

        result = businessDayConvention.adjust(
            date=date + period,
            calendar=self
        )

        return result

    def retreat(
            self,
            date: datetime.date,
            period: Period,
            businessDayConvention: BusinessDayConvention,
            endOfMonth: bool
    ):
        if endOfMonth and self.isLastMonthBusinessDay(date):
            return self.getLastMonthBusinessDay(date - period)

        result = businessDayConvention.adjust(
            date=date - period,
            calendar=self
        )

        return result
