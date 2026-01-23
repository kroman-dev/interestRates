from datetime import date
from unittest import TestCase

from ir.curve.discountCurve import DiscountCurve
from ir.dayCounter.act365Fixed import Act365Fixed
from ir.legs.fixedLeg import FixedLeg
from ir.legs.floatingLeg import FloatingLeg
from ir.products.swap import Swap
from ir.scheduler.businessDayConvention.noConvention import NoConvention
from ir.scheduler.calendar.noCalendar import NoCalendar
from ir.scheduler.schedule.schedule import Schedule
from ir.scheduler.stubPeriod.shortBack import ShortBack


class SwapTest(TestCase):

    def setUp(self):
        self._dayCounter = Act365Fixed
        self._effectiveDate = date(2022, 2, 14)
        self._terminationDate = date(2022, 6, 14)
        self._businessDayConvention = NoConvention()
        self._calendar = NoCalendar()
        self._stubPeriod = ShortBack()

        self._curve = DiscountCurve(
            dates=[date(2022, 1, 1), date(2022, 4, 1), date(2022, 7, 1)],
            discountFactors=[1., 0.9975, 0.9945],
            dayCounter=self._dayCounter
        )

        self._fixedSchedule = Schedule(
            effectiveDate=self._effectiveDate,
            terminationDate=self._terminationDate,
            frequency='4M',
            businessDayConvention=self._businessDayConvention,
            endOfMonth=False,
            stubPeriod=self._stubPeriod,
            calendar=self._calendar,
            paymentLag=0
        )

        self._floatingSchedule = Schedule(
            effectiveDate=self._effectiveDate,
            terminationDate=self._terminationDate,
            frequency='1M',
            businessDayConvention=self._businessDayConvention,
            endOfMonth=False,
            stubPeriod=self._stubPeriod,
            calendar=self._calendar,
            paymentLag=0
        )

        # parRate from book
        fixedRatePar = 1.1362747 / 100
        self._notional = 1e9

        fixedLeg1 = FixedLeg(
            fixedRate=fixedRatePar,
            discountCurve=self._curve,
            schedule=self._fixedSchedule,
            businessDayConvention=self._businessDayConvention,
            dayCounter=self._dayCounter,
            notional=self._notional
        )

        fixedLeg2 = FixedLeg(
            fixedRate=1.15 / 100,
            discountCurve=self._curve,
            schedule=self._fixedSchedule,
            businessDayConvention=self._businessDayConvention,
            dayCounter=self._dayCounter,
            notional=self._notional
        )

        floatingLeg = FloatingLeg(
            discountCurve=self._curve,
            schedule=self._floatingSchedule,
            businessDayConvention=self._businessDayConvention,
            dayCounter=self._dayCounter,
            notional=self._notional
        )

        self._swap1 = Swap(
            receiveLeg=floatingLeg,
            payLeg=fixedLeg1
        )

        self._swap2 = Swap(
            receiveLeg=floatingLeg,
            payLeg=fixedLeg2
        )

    def testParRate(self):
        self.assertAlmostEqual(
            0.,
            self._swap1.npv() / 1e9
        )

    def testNpv(self):
        self.assertAlmostEqual(
            -44901.21378,
            self._swap2.npv(),
            places=4
        )
