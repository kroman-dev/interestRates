from datetime import date
from unittest import TestCase

from ir import Act360, Act365Fixed
from ir.curve.discountCurve import DiscountCurve
from ir.products.deposit import Deposit
from ir.scheduler.businessDayConvention.noConvention import NoConvention
from ir.scheduler.calendar.noCalendar import NoCalendar
from ir.scheduler.stubPeriod.shortBack import ShortBack


class DepositTest(TestCase):

    def setUp(self):
        self._effectiveDate = date(2012, 12, 11)
        self._calendar = NoCalendar()
        self._stubPeriod = ShortBack()
        self._endOfMonth = False

        self._curve = DiscountCurve(
            dates=[self._effectiveDate, date(2012, 12, 12)],
            discountFactors=[1., 0.9999988888901234],
            dayCounter=Act365Fixed()
        )

        self._fixedRate = 0.04 / 100

        self._deposit = Deposit(
            curve=self._curve,
            fixedRate=self._fixedRate,
            effectiveDate=self._effectiveDate,
            tenor='1D',
            endOfMonth=False,
            businessDayConvention=NoConvention(),
            dayCounter=Act360(),
            stubPeriod=self._stubPeriod,
            calendar=self._calendar,
            notional=1.
        )

    def testParRate(self):
        with self.subTest("par rate from book"):
            self.assertAlmostEqual(
                self._fixedRate,
                self._deposit.getParRate(self._curve)
            )

        with self.subTest("par rate from book"):
            self.assertAlmostEqual(
                self._fixedRate,
                self._deposit.getParRate(self._curve)
            )

