from datetime import date
from unittest import TestCase

from ir.dayCounter.act365Fixed import Act365Fixed


class Act365FixedTest(TestCase):

    def testYearFraction(self):
        with self.subTest("year"):
            self.assertAlmostEqual(
                1.,
                Act365Fixed.yearFraction(
                    startDate=date(2025, 1, 1),
                    endDate=date(2026, 1, 1)
                )
            )
