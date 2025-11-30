from datetime import date
from unittest import TestCase

from ir.curve.discountCurve import DiscountCurve
from ir.dayCounter.thirty360BondBasis import Thirty360BondBasis


class DiscountCurveTest(TestCase):

    def setUp(self):
        dates = [date(2024, 1, 1), date(2024, 7, 1), date(2025, 1, 1)]
        discountFactors = [1.0, 0.98, 0.96]
        dayCounter = Thirty360BondBasis

        self._sampleCurve = DiscountCurve(
            dates=dates,
            discountFactors=discountFactors,
            dayCounter=dayCounter
        )

        self._sampleCurve2 = DiscountCurve(
            dates=[date(2025, 11, 3), date(2025, 11, 5), date(2025, 11, 7)],
            discountFactors=discountFactors,
            dayCounter=dayCounter
        )

        self._sampleCurve3 = DiscountCurve(
            dates=[date(2025, 11, 3), date(2026, 11, 5), date(2027, 11, 7)],
            discountFactors=discountFactors,
            dayCounter=dayCounter
        )

    def testInterpolate(self):
        with self.subTest("behavior"):
            self.assertGreater(self._sampleCurve(date(2024, 4, 1)), 0.98)
            self.assertLess(self._sampleCurve(date(2024, 4, 1)), 1.0)

        with self.subTest("left bound"):
            self.assertEqual(0.98, self._sampleCurve(date(2024, 7, 1)))

        with self.subTest("right bound"):
            self.assertEqual(0.96, self._sampleCurve(date(2025, 1, 1)))

    def testCompareWithQuantlib(self):
        with self.subTest("compare with quantlib"):
            self.assertAlmostEqual(
                0.9899494936611666,
                self._sampleCurve2(date(2025, 11, 4))
            )
        with self.subTest("compare with quantlib long distance"):
            self.assertAlmostEqual(
                0.9726039674627344,
                self._sampleCurve3(date(2027, 3, 18))
            )
