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
        self._holidays.append(datetime.date(2025, 12, 31))

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
        """
            # TODO think about eom and following case:
            # https://quant.stackexchange.com/questions/73827/is-end-of-month-eom-rule-overrides-convention-rule-in-quantlib-schedule
            # https://quant.stackexchange.com/questions/78641/is-end-of-month-eom-rule-overrides-unadjusted-convention-rule-in-quantlib
        """
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
