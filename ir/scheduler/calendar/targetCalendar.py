from workalendar.europe import EuropeanCentralBank

import datetime

from ir.scheduler.calendar.genericCalendar import GenericCalendar


class TargetCalendar(GenericCalendar):

    def __init__(self):
        super().__init__(name='TARGET')
        self._calendar = EuropeanCentralBank()

    def isBusinessDay(self, date: datetime.date) -> bool:
        return self._calendar.is_working_day(date)
