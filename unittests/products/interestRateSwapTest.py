from datetime import date
from unittest import TestCase

from ir.curve.discountCurve import DiscountCurve
from ir.dayCounter.act365Fixed import Act365Fixed
from ir.products.interestRateSwap import InterestRateSwap
from ir.scheduler.businessDayConvention.noConvention import NoConvention
from ir.scheduler.calendar.noCalendar import NoCalendar
from ir.scheduler.stubPeriod.shortBack import ShortBack


class SwapTest(TestCase):

    def setUp(self):
        self._dayCounter = Act365Fixed
        self._effectiveDate = date(2022, 2, 14)
        self._terminationDate = date(2022, 6, 14)
        self._businessDayConvention = NoConvention()
        self._calendar = NoCalendar()
        self._stubPeriod = ShortBack()
        self._fixFrequency = '4M'
        self._floatFrequency = '1M'
        self._endOfMonth = False

        self._curve = DiscountCurve(
            dates=[date(2022, 1, 1), date(2022, 4, 1), date(2022, 7, 1)],
            discountFactors=[1., 0.9975, 0.9945],
            dayCounter=self._dayCounter
        )

        # parRate from book
        fixedRatePar = 1.1362747 / 100
        fixedSomeRate = 1.15 / 100
        notional = 1e9

        self._swap1 = InterestRateSwap(
            curve=self._curve,
            fixedRate=fixedRatePar,
            effectiveDate=self._effectiveDate,
            terminationDate=self._terminationDate,
            fixFrequency=self._fixFrequency,
            floatFrequency=self._floatFrequency,
            endOfMonth=self._endOfMonth,
            businessDayConvention=self._businessDayConvention,
            dayCounter=self._dayCounter,
            stubPeriod=self._stubPeriod,
            calendar=self._calendar,
            notional=1.
        )

        self._swap2 = InterestRateSwap(
            curve=self._curve,
            fixedRate=fixedSomeRate,
            effectiveDate=self._effectiveDate,
            terminationDate=self._terminationDate,
            fixFrequency=self._fixFrequency,
            floatFrequency=self._floatFrequency,
            endOfMonth=self._endOfMonth,
            businessDayConvention=self._businessDayConvention,
            dayCounter=self._dayCounter,
            stubPeriod=self._stubPeriod,
            calendar=self._calendar,
            notional=notional
        )

    def testParRate(self):
        self.assertAlmostEqual(
            0.,
            self._swap1.npv()
        )

    def testNpv(self):

        self.assertAlmostEqual(
            -44901.21378,
            self._swap2.npv(),
            places=4
        )
