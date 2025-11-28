from unittest import TestCase
from datetime import date

from ir.scheduler.stubPeriod.shortFront import ShortFront


class ShortFrontTest(TestCase):

    def setUp(self):
        self._startDate = date(2025, 1, 1)
        self._endDate = date(2025, 4, 1)

    def testMakeSchedule(self):
        with self.subTest("simple 1M"):

            self.assertListEqual(
                [
                    date(2025, 1, 1),
                    date(2025, 2, 1),
                    date(2025, 3, 1),
                    date(2025, 4, 1)
                ],
                ShortFront.makeSchedule(
                    startDate=self._startDate,
                    endDate=self._endDate,
                    frequency='1M'
                )
            )


        with self.subTest("1W"):

            self.assertListEqual(
                [
                    date(2025, 1, 1),
                    date(2025, 1, 2),
                    date(2025, 1, 9)
                ],
                ShortFront.makeSchedule(
                    startDate=self._startDate,
                    endDate=date(2025, 1, 9),
                    frequency='1W'
                )
            )
