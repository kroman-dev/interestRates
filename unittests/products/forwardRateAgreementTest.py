from datetime import date
from unittest import TestCase

from ir.curve.discountCurve import DiscountCurve
from ir.dayCounter.act365Fixed import Act365Fixed
from ir.products.forwardRateAgreement import ForwardRateAgreement
from ir.scheduler.businessDayConvention.noConvention import NoConvention
from ir.scheduler.calendar.noCalendar import NoCalendar
from ir.scheduler.stubPeriod.shortBack import ShortBack


class ForwardRateAgreementTest(TestCase):

    def setUp(self):
        self._dayCounter = Act365Fixed()
        self._effectiveDate = date(2022, 1, 1)
        self._terminationDate = date(2022, 1, 21)
        self._businessDayConvention = NoConvention()
        self._calendar = NoCalendar()
        self._stubPeriod = ShortBack()
        self._frequency = '1M'
        self._endOfMonth = False

        self._curve = DiscountCurve(
            dates=[date(2022, 1, 1), date(2022, 1, 21)],
            discountFactors=[1., 0.9975],
            dayCounter=self._dayCounter
        )

        self._fixedRate = 1.1362747 / 100
        self.notional = 1e9

        self._fra1 = ForwardRateAgreement(
            fixedRate=self._fixedRate,
            effectiveDate=self._effectiveDate,
            terminationDate=self._terminationDate,
            frequency=self._frequency,
            endOfMonth=self._endOfMonth,
            businessDayConvention=self._businessDayConvention,
            dayCounter=self._dayCounter,
            stubPeriod=self._stubPeriod,
            calendar=self._calendar,
            notional=1.,
            discountCurve=self._curve
        )

    def testSchedule(self):
        with self.assertRaises(ValueError):
            ForwardRateAgreement(
                fixedRate=self._fixedRate,
                effectiveDate=self._effectiveDate,
                terminationDate=self._terminationDate,
                frequency='1D',
                endOfMonth=self._endOfMonth,
                businessDayConvention=self._businessDayConvention,
                dayCounter=self._dayCounter,
                stubPeriod=self._stubPeriod,
                calendar=self._calendar,
                notional=1.,
                discountCurve=self._curve
            )

    def testNpv(self):
        accrual = 20 / 365
        forward = (1 / 0.9975 - 1) / accrual
        self.assertAlmostEqual(
            0.9975 * accrual * (forward - self._fixedRate),
            self._fra1.npv()
        )

    def testGetParRate(self):
        self.assertAlmostEqual(
            (1 / 0.9975 - 1) / (20 / 365),
            self._fra1.getParRate()
        )


