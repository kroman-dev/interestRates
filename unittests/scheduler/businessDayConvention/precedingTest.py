import datetime

from unittest import TestCase

from ir.scheduler.businessDayConvention.preceding import Preceding
from ir.scheduler.calendar.russiaCalendar import RussiaCalendar


class PrecedingTest(TestCase):

    def setUp(self):
        self._testDate = datetime.date(2025, 11, 23)
        self._calendar = RussiaCalendar()

    def testAdjust(self):
        self.assertEqual(
            datetime.date(2025, 11, 21),
            Preceding.adjust(self._testDate, self._calendar)
        )
