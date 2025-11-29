import datetime

from unittest import TestCase

from ir.scheduler.businessDayConvention.modifiedFollowing import \
    ModifiedFollowing
from ir.scheduler.calendar.russiaCalendar import RussiaCalendar


class ModifiedFollowingTest(TestCase):

    def setUp(self):
        self._testDate = datetime.date(2025, 11, 29)
        self._calendar = RussiaCalendar()

    def testAdjust(self):
        with self.subTest("back"):
            self.assertEqual(
                datetime.date(2025, 11, 28),
                ModifiedFollowing.adjust(self._testDate, self._calendar)
            )

        with self.subTest('front'):
            self.assertEqual(
                datetime.date(2025, 11, 24),
                ModifiedFollowing.adjust(
                    datetime.date(2025, 11, 23),
                    self._calendar
                )
            )
