import datetime
try:
    import holidays_ru
except:
    raise ImportError('Cant import holidays_ru -> install')

from ir.scheduler.businessDayConvention.businessDayConvention import \
    BusinessDayConvention
from ir.scheduler.calendar.genericCalendar import GenericCalendar
from ir.scheduler.period.period import Period


class RussiaCalendar(GenericCalendar):

    def __init__(self):
        super().__init__(name='Russia')

    def isBusinessDay(self, date: datetime.date) -> bool:
        return holidays_ru.check_holiday(date)

    def isEndOfMonth(self, date: datetime.date) -> bool:
        pass

    def getEndOfMonth(self, date: datetime.date) -> datetime.date:
        pass

    def advance(
            self,
            date: datetime.date,
            period: Period,
            businessDayConvention: BusinessDayConvention,
            endOfMonth: bool
    ):
        pass
