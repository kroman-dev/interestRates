from unittest import TestCase
from datetime import date

from ir.scheduler.businessDayConvention.following import Following
from ir.scheduler.calendar.russiaCalendar import RussiaCalendar
from ir.scheduler.stubPeriod.shortFront import ShortFront


class ShortFrontTest(TestCase):

    def setUp(self):
        self._startDate = date(2025, 2, 1)
        self._endDate = date(2025, 6, 1)

    def testMakeSchedule(self):
        with self.subTest("simple 1M"):
            self.assertListEqual(
                [
                    date(2025, 2, 3),
                    date(2025, 3, 3),
                    date(2025, 4, 1),
                    date(2025, 5, 2),
                    date(2025, 6, 2)
                ],
                ShortFront.makeSchedule(
                    startDate=self._startDate,
                    endDate=self._endDate,
                    frequency='1M',
                    calendar=RussiaCalendar(),
                    businessDayConvention=Following(),
                    endOfMonth=False
                )
            )

        with self.subTest("with stub"):
            self.assertListEqual(
                [
                    date(2025, 2, 3),
                    date(2025, 2, 17),
                    date(2025, 3, 17),
                    date(2025, 4, 15),
                    date(2025, 5, 15),
                    date(2025, 6, 16)
                ],
                ShortFront.makeSchedule(
                    startDate=self._startDate,
                    endDate=date(2025, 6, 15),
                    frequency='1M',
                    calendar=RussiaCalendar(),
                    businessDayConvention=Following(),
                    endOfMonth=False
                )
            )
