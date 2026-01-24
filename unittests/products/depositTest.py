from datetime import date
from unittest import TestCase

from ir import Act360, Following, TargetCalendar
from ir.curve.discountCurve import DiscountCurve
from ir.products.deposit import Deposit
from ir.scheduler.stubPeriod.shortBack import ShortBack


class DepositTest(TestCase):

    def setUp(self):
        self._effectiveDate = date(2012, 12, 11)
        self._calendar = TargetCalendar()
        self._stubPeriod = ShortBack()
        self._endOfMonth = False

        self._curve = DiscountCurve(
            dates=[
                self._effectiveDate, date(2012, 12, 12), date(2012, 12, 13)
            ],
            discountFactors=[1., 0.9999988888901234, 0.9999977777814815],
            dayCounter=Act360()
        )

        self._fixedRate = 0.04 / 100

        self._sampleDeposit1 = Deposit(
            curve=self._curve,
            fixedRate=self._fixedRate,
            effectiveDate=self._effectiveDate,
            tenor='1D',
            endOfMonth=False,
            businessDayConvention=Following(),
            dayCounter=Act360(),
            stubPeriod=self._stubPeriod,
            calendar=self._calendar,
            notional=1.
        )

        self._sampleDeposit2 = Deposit(
            curve=self._curve,
            fixedRate=self._fixedRate,
            effectiveDate=date(2012, 12, 12),
            tenor='1D',
            endOfMonth=False,
            businessDayConvention=Following(),
            dayCounter=Act360(),
            stubPeriod=self._stubPeriod,
            calendar=self._calendar,
            notional=1.
        )

    def testParRate(self):
        with self.subTest("par rate from the article 1"):
            self.assertAlmostEqual(
                self._fixedRate,
                self._sampleDeposit1.getParRate(self._curve)
            )

        with self.subTest("par rate from the article 2"):
            self.assertAlmostEqual(
                self._fixedRate,
                self._sampleDeposit2.getParRate(self._curve)
            )

