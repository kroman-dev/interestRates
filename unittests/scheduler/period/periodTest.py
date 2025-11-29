import datetime

from unittest import TestCase

from ir.scheduler.period.period import Period


class PeriodTest(TestCase):

    def setUp(self):
        self._testDate = datetime.date(2025, 1, 1)

    def testAdvance(self):
        with self.subTest("1D"):
            self.assertEqual(
                datetime.date(2025, 1, 2),
                Period("1D").advance(self._testDate)
            )

        with self.subTest("1w"):
            self.assertEqual(
                datetime.date(2025, 1, 8),
                Period("1w").advance(self._testDate)
            )

    def testRightAdd(self):
        with self.subTest("1D"):
            self.assertEqual(
                datetime.date(2025, 1, 2),
                self._testDate + Period("1D")
            )

        with self.subTest("1w"):
            self.assertEqual(
                datetime.date(2025, 1, 8),
                self._testDate + Period("1w")
            )

        with self.subTest("period sum"):
            newPeriod = Period("2w") + Period("1w")
            self.assertEqual(
                datetime.date(2025, 1, 22),
                self._testDate + newPeriod
            )

    def testLeftAdd(self):
        with self.subTest("1D"):
            self.assertEqual(
                datetime.date(2025, 1, 2),
                Period("1D") + self._testDate
            )

        with self.subTest("1w"):
            self.assertEqual(
                datetime.date(2025, 1, 8),
                Period("1w") + self._testDate
            )

    def testRetreat(self):
        with self.subTest("1D"):
            self.assertEqual(
                datetime.date(2025, 1, 1),
                datetime.date(2025, 1, 2) - Period("1D")
            )
