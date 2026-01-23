from datetime import date
from unittest import TestCase

from ir.curve.curveBootstrapping import CurveBootstrapping
from ir.curve.discountCurve import DiscountCurve
from ir.curve.interpolator.logLinearInterpolator import LogLinearInterpolator
from ir.dayCounter.act365Fixed import Act365Fixed
from ir.products.interestRateSwap import InterestRateSwap
from ir.scheduler.businessDayConvention.noConvention import NoConvention
from ir.scheduler.calendar.noCalendar import NoCalendar
from ir.scheduler.stubPeriod.shortBack import ShortBack


class CurveBootstrappingTest(TestCase):

    def setUp(self):
        self._dayCounter = Act365Fixed
        self._effectiveDate = date(2022, 1, 1)
        self._businessDayConvention = NoConvention()
        self._calendar = NoCalendar()
        self._stubPeriod = ShortBack()
        self._fixFrequency = '1Y'
        self._floatFrequency = '1Y'
        self._endOfMonth = False

        dates = [
            date(2022, 1, 1),
            date(2023, 1, 1),
            date(2024, 1, 1),
            date(2027, 1, 1),
            date(2032, 1, 1)
        ]
        values = [1. for _ in range(len(dates))]

        self._initialNodes = {
            _date: discountFactor
            for _date, discountFactor in zip(dates, values)
        }

        self._initialCurve = DiscountCurve(
            dates=dates,
            discountFactors=values,
            dayCounter=self._dayCounter
        )

        createSwap = lambda fixedRate, terminationDate: InterestRateSwap(
            curve=self._initialCurve,
            fixedRate=fixedRate,
            effectiveDate=self._effectiveDate,
            terminationDate=terminationDate,
            fixFrequency=self._fixFrequency,
            floatFrequency=self._floatFrequency,
            endOfMonth=self._endOfMonth,
            businessDayConvention=self._businessDayConvention,
            dayCounter=self._dayCounter,
            stubPeriod=self._stubPeriod,
            calendar=self._calendar,
            notional=1.
        )

        self._swapQuotes = [
            quote / 100 for quote in [1.210, 1.635, 1.885, 1.930]
        ]

        self._swaps = [
            createSwap(fixRate, endDate)
            for fixRate, endDate in zip(self._swapQuotes, dates[1:])
        ]

        self._targetCurve = DiscountCurve(
            dates=dates,
            discountFactors=[
                1.,
                0.9880446596186105,
                0.9680183694743251,
                0.9105211762541432,
                0.8254636028183167
            ],
            dayCounter=self._dayCounter
        )

    def testSolve(self):
        curve, convergenceStatus = CurveBootstrapping(
            initialGuessNodes=self._initialNodes,
            swaps=self._swaps,
            dayCounter=self._dayCounter,
            curveInterpolator=LogLinearInterpolator
        ).solve()

        self.assertTrue(convergenceStatus)

        for swap in self._swaps:
            with self.subTest(f"{swap.getFixedRate()}"):
                self.assertAlmostEqual(
                    0,
                    swap.npv(curve).realPart
                )
