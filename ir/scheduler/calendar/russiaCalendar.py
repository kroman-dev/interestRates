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
        self._holidays.append(datetime.date(2025, 11, 3))
        self._holidays.append(datetime.date(2025, 11, 4))

    def isBusinessDay(self, date: datetime.date) -> bool:
        if date in self._holidays:
            return False
        return not holidays_ru.check_holiday(date)

    def advance(
            self,
            date: datetime.date,
            period: Period,
            businessDayConvention: BusinessDayConvention,
            endOfMonth: bool
    ):

        result = businessDayConvention.adjust(
            date=date + period,
            calendar=self
        )
        if (result.month != (date + period).month) and endOfMonth:
            raise NotImplementedError('warning case')

        if endOfMonth:
            return self.getEndOfMonth(result)

        return result

    def retreat(
            self,
            date: datetime.date,
            period: Period,
            businessDayConvention: BusinessDayConvention,
            endOfMonth: bool
    ):
        result = businessDayConvention.adjust(
            date=date - period,
            calendar=self
        )
        if (result.month != (date - period).month) and endOfMonth:
            raise NotImplementedError('warning case')

        if endOfMonth:
            return self.getEndOfMonth(result)

        return result
