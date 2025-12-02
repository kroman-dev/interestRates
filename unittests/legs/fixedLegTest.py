from datetime import date
from unittest import TestCase
from unittest.mock import Mock

from ir.curve.discountCurve import DiscountCurve
from ir.dayCounter.thirty360BondBasis import Thirty360BondBasis
from ir.legs.fixedLeg import FixedLeg
from ir.scheduler.businessDayConvention.noConvention import NoConvention
from ir.scheduler.schedule.genericSchedule import GenericSchedule
from ir.scheduler.schedule.scheduleData import ScheduleData


class FixedLegTest(TestCase):

    def setUp(self):
        self._dayCounter = Thirty360BondBasis
        self._curveDates = [
            date(2024, 1, 1),
            date(2024, 7, 1),
            date(2025, 1, 1)
        ]
        self._discountFactors = [1.0, 0.75, 0.5]
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

        self._fixedRate = 0.5

        self._fixedLeg = FixedLeg(
            fixedRate=self._fixedRate,
            curve=self._curve,
            schedule=self._schedule,
            businessDayConvention=self._businessDayConvention,
            dayCounter=self._dayCounter
        )

    def testCashFlows(self):
        self.assertListEqual(
            [0.1875, 0.125],
            self._fixedLeg.getCashFlows()
        )

