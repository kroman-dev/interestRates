from unittest import TestCase
from datetime import date

from ir.scheduler.stubPeriod.shortBack import ShortBack


class ShortBackTest(TestCase):

    def setUp(self):
        self._startDate = date(2025, 2, 1)
        self._endDate = date(2025, 6, 1)

    def testMakeSchedule(self):
        with self.subTest("simple 1M"):
            self.assertListEqual(
                [
                    date(2025, 2, 1),
                    date(2025, 3, 1),
                    date(2025, 4, 1),
                    date(2025, 5, 1),
                    date(2025, 6, 1)
                ],
                ShortBack.makeUnadjustedSchedule(
                    startDate=self._startDate,
                    endDate=self._endDate,
                    frequency='1M'
                )
            )

        with self.subTest("simple 1M"):
            self.assertListEqual(
                [
                    date(2025, 2, 1),
                    date(2025, 3, 1),
                    date(2025, 4, 1),
                    date(2025, 5, 1),
                    date(2025, 6, 1),
                    date(2025, 6, 15)
                ],
                ShortBack.makeUnadjustedSchedule(
                    startDate=self._startDate,
                    endDate=date(2025, 6, 15),
                    frequency='1M'
                )
            )

        with self.subTest("1W"):
            # TODO warning case?
            self.assertListEqual(
                [
                    date(2025, 1, 1),
                    date(2025, 1, 8),
                    date(2025, 1, 10)
                ],
                ShortBack.makeUnadjustedSchedule(
                    startDate=date(2025, 1, 1),
                    endDate=date(2025, 1, 10),
                    frequency='1W'
                )
            )
