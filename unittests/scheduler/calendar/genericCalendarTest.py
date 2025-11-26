import datetime

from unittest import TestCase

from ir.scheduler.businessDayConvention.businessDayConvention import \
    BusinessDayConvention
from ir.scheduler.calendar.genericCalendar import GenericCalendar
from ir.scheduler.period.period import Period


class SomeCalendar(GenericCalendar):

    def isBusinessDay(self, date: datetime.date) -> bool:
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

    def __init__(self):
        super().__init__('Some')


class GenericCalendarTest(TestCase):

    def testIsEndOfMonth(self):
        with self.subTest('true'):
            self.assertEqual(
                True,
                SomeCalendar.isEndOfMonth(datetime.date(2025, 11, 30))
            )

        with self.subTest('false'):
            self.assertEqual(
                False,
                SomeCalendar.isEndOfMonth(datetime.date(2025, 11, 10))
            )
