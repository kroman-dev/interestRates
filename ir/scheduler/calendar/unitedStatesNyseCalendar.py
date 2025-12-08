import datetime
import exchange_calendars as ec

from ir.scheduler.calendar.genericCalendar import GenericCalendar


class UnitedStatesNyseCalendar(GenericCalendar):

    def __init__(self):
        super().__init__(name='UnitedStatesNyse')
        self._nyseCalendar = ec.get_calendar(
            'XNYS',
            start=datetime.date(2020, 1, 1),
            end=datetime.date(2055, 1, 1)
        )

    def isBusinessDay(self, date: datetime.date) -> bool:
        return self._nyseCalendar.is_session(date)
