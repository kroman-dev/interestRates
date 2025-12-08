from datetime import date
from unittest import TestCase

from ir.dayCounter.act360 import Act360


class Act365FixedTest(TestCase):

    def testYearFraction(self):
        with self.subTest("year"):
            self.assertAlmostEqual(
                365/360,
                Act360.yearFraction(
                    startDate=date(2025, 1, 1),
                    endDate=date(2026, 1, 1)
                )
            )
