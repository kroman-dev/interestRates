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
        self._dayCounter = Act365Fixed()
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
        self._fixedRatePar = 1.1362747 / 100
        fixedSomeRate = 1.15 / 100
        self.notional = 1e9

        self._swap1 = InterestRateSwap(
            discountCurve=self._curve,
            fixedRate=self._fixedRatePar,
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
            notional=self.notional
        )

        dates = [
            date(2022, 1, 1),
            date(2023, 1, 1),
            date(2024, 1, 1),
            date(2027, 1, 1),
            date(2032, 1, 1)
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

        self._fixedRates = [
            quote / 100 for quote in [1.210, 1.635, 1.885, 1.930]
        ]

        createSwap = lambda fixedRate, terminationDate, discountCurve = None:\
            InterestRateSwap(
                fixedRate=fixedRate,
                effectiveDate=date(2022, 1, 1),
                terminationDate=terminationDate,
                fixFrequency='1Y',
                floatFrequency='1Y',
                endOfMonth=self._endOfMonth,
                businessDayConvention=self._businessDayConvention,
                dayCounter=self._dayCounter,
                stubPeriod=self._stubPeriod,
                calendar=self._calendar,
                notional=1.,
                discountCurve=discountCurve
        )
        self._swaps = [
            createSwap(fixRate, endDate)
            for fixRate, endDate in zip(self._fixedRates, dates[1:])
        ]

        self._swaps2 = [
            createSwap(fixRate, endDate, self._targetCurve)
            for fixRate, endDate in zip(self._fixedRates, dates[1:])
        ]


    def testParRate(self):
        with self.subTest("par rate from book"):
            self.assertAlmostEqual(
                0.,
                self._swap1.npv()
            )

        with self.subTest("get numerical par rate"):
            self.assertAlmostEqual(
                self._fixedRatePar,
                self._swap2.getParRate(
                    self._curve
                )
            )

        with self.subTest("get numerical par rate"):
            self.assertAlmostEqual(
                0.,
                self._swap2.getParRate(
                    DiscountCurve(
                        dates=[date(2022, 1, 1), date(2022, 4, 1),
                               date(2022, 7, 1)],
                        discountFactors=[1., 1., 1.],
                        dayCounter=self._dayCounter
                    )
                )
            )

        for swap in self._swaps:
            with self.subTest(f"{swap._payLeg.getFixedRate()}"):
                self.assertAlmostEqual(
                    swap._payLeg.getFixedRate(),
                    swap.getParRate(self._targetCurve)
                )


        for swap in self._swaps2:
            with self.subTest(f"{swap._payLeg.getFixedRate()}"):
                self.assertAlmostEqual(
                    swap._payLeg.getFixedRate(),
                    swap.getParRate(self._targetCurve)
                )

    def testNpv(self):
        with self.subTest('internal'):
            self.assertAlmostEqual(
                -44901.21378,
                self._swap2.npv(self._curve),
                places=4
            )

        with self.subTest('external'):
            self.assertAlmostEqual(
                -self.notional * self._swap2._payLeg.getFixedRate() \
                * self._swap2._payLeg._accrualYearFractions[0],
                self._swap2.npv(
                    DiscountCurve(
                        dates=[
                            date(2022, 1, 1),
                            date(2022, 4, 1),
                            date(2022, 7, 1)
                        ],
                        discountFactors=[1., 1., 1.],
                        dayCounter=self._dayCounter
                    )
                ),
                places=4
            )

        for swap in self._swaps:
            with self.subTest(f"{swap._payLeg.getFixedRate()}"):
                self.assertAlmostEqual(
                    0.,
                    swap.npv(self._targetCurve)
                )

    def testMultiCurve(self):
        forwardCurve = DiscountCurve(
            dates=[date(2022, 1, 1), date(2022, 1, 21)],
            discountFactors=[1., 0.9975],
            dayCounter=self._dayCounter
        )
        accrual = 20 / 365
        forward = (1 / 0.9975 - 1) / accrual
        expectedValue = self._curve.getDiscountFactor(date(2022, 1, 21)) \
                        * accrual * (forward - self._fixedRatePar)
        swapMultiCurve = InterestRateSwap(
            discountCurve=self._curve,
            fixedRate=self._fixedRatePar,
            effectiveDate=date(2022, 1, 1),
            terminationDate=date(2022, 1, 21),
            fixFrequency='20D',
            floatFrequency='20D',
            endOfMonth=self._endOfMonth,
            businessDayConvention=self._businessDayConvention,
            dayCounter=self._dayCounter,
            stubPeriod=self._stubPeriod,
            calendar=self._calendar,
            notional=1.
        )
        self.assertAlmostEqual(
            expectedValue,
            swapMultiCurve.npv(forwardCurve)
        )
