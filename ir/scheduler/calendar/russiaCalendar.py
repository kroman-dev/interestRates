import datetime
try:
    import holidays_ru
except:
    raise ImportError('Cant import holidays_ru -> install')

from ir.scheduler.calendar.genericCalendar import GenericCalendar


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
