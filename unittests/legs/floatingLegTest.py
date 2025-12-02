import numpy as np

from datetime import date
from unittest import TestCase
from unittest.mock import Mock

from ir.curve.discountCurve import DiscountCurve
from ir.dayCounter.thirty360BondBasis import Thirty360BondBasis
from ir.legs.floatingLeg import FloatingLeg
from ir.scheduler.businessDayConvention.noConvention import NoConvention
from ir.scheduler.schedule.genericSchedule import GenericSchedule
from ir.scheduler.schedule.scheduleData import ScheduleData


class FloatingLegTest(TestCase):

    def setUp(self):
        self._dayCounter = Thirty360BondBasis
        self._curveDates = [
            date(2024, 1, 1),
            date(2024, 7, 1),
            date(2025, 1, 1)
        ]
        self._discountFactors = [1.0, 0.8, 0.5]
        self._curve = DiscountCurve(
            dates=self._curveDates,
            discountFactors=self._discountFactors,
            dayCounter=self._dayCounter
        )

        self._businessDayConvention = NoConvention()

        self._scheduleData = ScheduleData(
            accrualStartDates=[date(2024, 1, 1), date(2024, 7, 1)],
            accrualEndDates=[date(2024, 7, 1), date(2025, 1, 1)],
            paymentDates=[date(2024, 7, 1), date(2025, 1, 1)]
        )

        self._schedule = Mock(spec=GenericSchedule)
        self._schedule.getSchedule.return_value = self._scheduleData

        self._floatingLeg = FloatingLeg(
            curve=self._curve,
            schedule=self._schedule,
            businessDayConvention=self._businessDayConvention,
            dayCounter=self._dayCounter
        )

    def testCashFlows(self):
        np.testing.assert_array_almost_equal(
            [0.2, 0.3],
            self._floatingLeg.getCashFlows()
        )
