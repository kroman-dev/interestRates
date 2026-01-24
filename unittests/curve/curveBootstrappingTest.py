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
        self._dayCounter = Act365Fixed()

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

        createSwap = lambda fixedRate, terminationDate, discountCurve = None:\
            InterestRateSwap(
                fixedRate=fixedRate,
                effectiveDate=date(2022, 1, 1),
                terminationDate=terminationDate,
                fixFrequency='1Y',
                floatFrequency='1Y',
                endOfMonth=False,
                businessDayConvention=NoConvention(),
                dayCounter=self._dayCounter,
                stubPeriod=ShortBack(),
                calendar=NoCalendar(),
                notional=1.,
                discountCurve=discountCurve
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
        self._swaps2 = [
            createSwap(fixRate, endDate, self._targetCurve)
            for fixRate, endDate in zip(self._swapQuotes, dates[1:])
        ]

    def testSolve1(self):
        curve, convergenceStatus = CurveBootstrapping(
            initialGuessNodes=self._initialNodes,
            instruments=self._swaps,
            instrumentsQuotes=self._swapQuotes,
            dayCounter=self._dayCounter,
            curveInterpolator=LogLinearInterpolator
        ).solve()

        self.assertTrue(convergenceStatus)

        for swap, quote in zip(self._swaps, self._swapQuotes):
            with self.subTest(f"{quote}"):
                self.assertAlmostEqual(
                    0,
                    swap.npv(curve).realPart
                )

    def testSolve2(self):
        curve, convergenceStatus = CurveBootstrapping(
            initialGuessNodes=self._initialNodes,
            instruments=self._swaps2,
            instrumentsQuotes=self._swapQuotes,
            dayCounter=self._dayCounter,
            curveInterpolator=LogLinearInterpolator
        ).solve()

        self.assertTrue(convergenceStatus)

        for swap, quote in zip(self._swaps2, self._swapQuotes):
            with self.subTest(f"{quote}"):
                self.assertAlmostEqual(
                    0,
                    swap.npv(curve).realPart
                )
