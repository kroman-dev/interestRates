from datetime import date
from unittest import TestCase

from ir import Thirty360BondBasis
from ir.curve.discountCurve import DiscountCurve
from ir.index.euribor3m import Euribor3M
from ir.products.indexInterestRateSwap import IndexInterestRateSwap
from ir.scheduler.stubPeriod.shortBack import ShortBack


class IndexInterestRateSwapTest(TestCase):

    def setUp(self):
        self._index = Euribor3M()
        self._effectiveDate = date(2022, 2, 14)
        self._terminationDate = date(2022, 8, 14)
        self._dayCounter = Thirty360BondBasis()
        self._stubPeriod = ShortBack()
        self._fixFrequency = '6M'
        self._fixedRate = 0.01

        self._curve = DiscountCurve(
            dates=[date(2022, 1, 1), date(2022, 4, 1), date(2022, 7, 1)],
            discountFactors=[1., 0.9975, 0.9945],
            dayCounter=Euribor3M().getDayCounter()
        )

        self._swap = IndexInterestRateSwap(
            index=self._index,
            fixedRate=self._fixedRate,
            effectiveDate=self._effectiveDate,
            terminationDate=self._terminationDate,
            dayCounter=self._dayCounter,
            fixFrequency=self._fixFrequency,
            stubPeriod=self._stubPeriod,
            discountCurve=self._curve
        )

    def testIndexParameters(self):
        """Test that swap correctly uses index parameters"""
        # Check that float frequency is taken from index tenor
        self.assertEqual(
            self._index.getTenor(),
            self._swap._receiveLeg._schedule._frequency
        )
        
        # Check that business day convention is from index
        self.assertEqual(
            self._index.getBusinessDayConvention(),
            self._swap._receiveLeg._schedule._businessDayConvention
        )
        
        # Check that calendar is from index
        self.assertEqual(
            self._index.getCalendar(),
            self._swap._receiveLeg._schedule._calendar
        )
        
        # Check that endOfMonth is from index
        self.assertEqual(
            self._index.getEndOfMonth(),
            self._swap._receiveLeg._schedule._endOfMonth
        )
        
        # Check that dayCounter is from index
        self.assertEqual(
            self._dayCounter,
            self._swap._payLeg._dayCounter
        )

        self.assertEqual(
            self._index.getDayCounter(),
            self._swap._receiveLeg._dayCounter
        )
