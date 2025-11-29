import datetime

from unittest import TestCase

from ir.scheduler.businessDayConvention.following import Following
from ir.scheduler.calendar.russiaCalendar import RussiaCalendar


class FollowingTest(TestCase):

    def setUp(self):
        self._testDate = datetime.date(2025, 11, 23)
        self._calendar = RussiaCalendar()

    def testAdjust(self):
        self.assertEqual(
            datetime.date(2025, 11, 24),
            Following.adjust(self._testDate, self._calendar)
        )
