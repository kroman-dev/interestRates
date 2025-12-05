from typing import Optional

import numpy as np

from ir.curve.discountCurve import DiscountCurve
from ir.legs.genericLeg import GenericLeg
from ir.dayCounter.genericDayCounter import GenericDayCounter
from ir.projectTyping.floatVectorType import FloatVectorType
from ir.scheduler.businessDayConvention.genericBusinessDayConvention import \
    GenericBusinessDayConvention
from ir.scheduler.schedule.genericSchedule import GenericSchedule


class FixedLeg(GenericLeg):

    def __init__(
            self,
            fixedRate: float,
            curve: DiscountCurve,
            schedule: GenericSchedule,
            businessDayConvention: GenericBusinessDayConvention,
            dayCounter: GenericDayCounter,
            notional: float = 1.
    ):
        super().__init__(
            curve=curve,
            schedule=schedule,
            businessDayConvention=businessDayConvention,
            dayCounter=dayCounter,
            notional=notional
        )
        self._fixedRate = fixedRate

    def getFixRate(self) -> float:
        return self._fixedRate

    def getCashFlows(
            self,
            curve: Optional[DiscountCurve] = None
    ) -> FloatVectorType:
        discountFactors = self._discountFactors

        if curve is not None:
            discountFactors = np.array([
                curve.getDiscountFactor(paymentDate)
                for paymentDate in self._scheduleData.paymentDates
            ])

        return self._notional * self._fixedRate \
            * self._accrualYearFractions * discountFactors
