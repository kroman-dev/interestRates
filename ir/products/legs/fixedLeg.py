from typing import Optional

from ir.curve.genericCurve import GenericCurve
from ir.products.legs.genericLeg import GenericLeg
from ir.dayCounter.genericDayCounter import GenericDayCounter
from ir.projectTyping.floatVectorType import FloatVectorType
from ir.scheduler.schedule.genericSchedule import GenericSchedule


class FixedLeg(GenericLeg):

    def __init__(
            self,
            fixedRate: float,
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
        self._fixedRate = fixedRate

    def getFixedRate(self) -> float:
        return self._fixedRate

    def getCashFlows(
            self,
            discountCurve: Optional[GenericCurve] = None,
            forwardCurve: Optional[GenericCurve] = None
    ) -> FloatVectorType:
        return self._notional * self._fixedRate \
            * self._accrualYearFractions * self.getDiscountFactors(
                discountCurve
            )
