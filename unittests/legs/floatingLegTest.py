import numpy as np

from datetime import date
from unittest import TestCase
from unittest.mock import Mock

from ir.curve.discountCurve import DiscountCurve
from ir.dayCounter.thirty360BondBasis import Thirty360BondBasis
from ir.legs.floatingLeg import FloatingLeg
from ir.scheduler.schedule.genericSchedule import GenericSchedule
from ir.scheduler.schedule.scheduleData import ScheduleData


class FloatingLegTest(TestCase):

    def setUp(self):
        self._dayCounter = Thirty360BondBasis
        self._curve = DiscountCurve(
            dates=[
                date(2024, 1, 1),
                date(2024, 7, 1),
                date(2025, 1, 1)
            ],
            discountFactors=[1.0, 0.8, 0.5],
            dayCounter=self._dayCounter
        )

        self._scheduleData = ScheduleData(
            accrualStartDates=[date(2024, 1, 1), date(2024, 7, 1)],
            accrualEndDates=[date(2024, 7, 1), date(2025, 1, 1)],
            paymentDates=[date(2024, 7, 1), date(2025, 1, 1)]
        )

        self._schedule = Mock(spec=GenericSchedule)
        self._schedule.getSchedule.return_value = self._scheduleData

        self._sampleLeg1 = FloatingLeg(
            schedule=self._schedule,
            dayCounter=self._dayCounter
        )
        self._sampleLeg2 = FloatingLeg(
            schedule=self._schedule,
            dayCounter=self._dayCounter,
            discountCurve=self._curve
        )

    def testCashFlows(self):
        expectedAnswer = [0.2, 0.3]
        with self.subTest("with input curve"):
            np.testing.assert_array_almost_equal(
                expectedAnswer,
                self._sampleLeg1.getCashFlows(self._curve)
            )
        with self.subTest("with internal curve"):
            np.testing.assert_array_almost_equal(
                expectedAnswer,
                self._sampleLeg2.getCashFlows()
            )
