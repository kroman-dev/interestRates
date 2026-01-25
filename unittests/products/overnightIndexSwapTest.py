from datetime import date
from unittest import TestCase

from ir.curve.discountCurve import DiscountCurve
from ir.dayCounter.act360 import Act360
from ir.index.eonia import Eonia
from ir.products.overnightIndexSwap import OvernightIndexSwap
from ir.scheduler.stubPeriod.shortBack import ShortBack


class OvernightIndexSwapTest(TestCase):

    def setUp(self):
        self._index = Eonia()
        self._dayCounter = Act360()
        self._effectiveDate = date(2022, 2, 14)
        self._terminationDate = date(2022, 8, 14)
        self._stubPeriod = ShortBack()
        self._fixFrequency = '3M'
        self._fixedRate = 0.01

        self._curve = DiscountCurve(
            dates=[date(2022, 1, 1), date(2022, 4, 1), date(2022, 7, 1)],
            discountFactors=[1., 0.9975, 0.9945],
            dayCounter=self._dayCounter
        )

        self._swap = OvernightIndexSwap(
            index=self._index,
            fixedRate=self._fixedRate,
            effectiveDate=self._effectiveDate,
            terminationDate=self._terminationDate,
            fixFrequency=self._fixFrequency,
            stubPeriod=self._stubPeriod,
            discountCurve=self._curve
        )

    def testOvernightIndexParameters(self):
        """Test that swap correctly uses overnight index parameters"""
        # Check that float frequency is set to fixFrequency (not index tenor)
        self.assertEqual(
            self._fixFrequency,
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
            self._index.getDayCounter(),
            self._swap._receiveLeg._dayCounter
        )
        
        # Check that index tenor is 1D (overnight)
        self.assertEqual(
            '1D',
            self._index.getTenor()
        )
