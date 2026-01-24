from typing import Optional

from ir.curve.genericCurve import GenericCurve
from ir.dayCounter.genericDayCounter import GenericDayCounter
from ir.legs.genericLeg import GenericLeg
from ir.projectTyping.floatVectorType import FloatVectorType
from ir.scheduler.schedule.genericSchedule import GenericSchedule


class FloatingLeg(GenericLeg):

    def __init__(
            self,
            schedule: GenericSchedule,
            dayCounter: GenericDayCounter,
            notional: float = 1.,
            discountCurve: Optional[GenericCurve] = None,
            forwardCurve: Optional[GenericCurve] = None
    ):
        super().__init__(
            schedule=schedule,
            dayCounter=dayCounter,
            notional=notional,
            discountCurve=discountCurve,
            forwardCurve=forwardCurve
        )

    def _getCashFlows(
            self,
            discountCurve: Optional[GenericCurve] = None,
            forwardCurve: Optional[GenericCurve] = None
    ) -> FloatVectorType:
        return self._notional * self.getForwardRates(forwardCurve) \
            * self.getDiscountFactors(discountCurve) \
            * self._accrualYearFractions
