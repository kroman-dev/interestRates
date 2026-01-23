from typing import Optional

from ir.curve.genericCurve import GenericCurve
from ir.dayCounter.genericDayCounter import GenericDayCounter
from ir.legs.genericLeg import GenericLeg
from ir.projectTyping.floatVectorType import FloatVectorType
from ir.scheduler.businessDayConvention.genericBusinessDayConvention import \
    GenericBusinessDayConvention
from ir.scheduler.schedule.genericSchedule import GenericSchedule


class FloatingLeg(GenericLeg):

    def __init__(
            self,
            schedule: GenericSchedule,
            businessDayConvention: GenericBusinessDayConvention,
            dayCounter: GenericDayCounter,
            notional: float = 1.,
            discountCurve: Optional[GenericCurve] = None,
            forwardCurve: Optional[GenericCurve] = None
    ):
        super().__init__(
            schedule=schedule,
            businessDayConvention=businessDayConvention,
            dayCounter=dayCounter,
            notional=notional,
            discountCurve=discountCurve,
            forwardCurve=forwardCurve
        )

    def getCashFlows(
            self,
            curve: Optional[GenericCurve] = None
    ) -> FloatVectorType:
        return self._notional * self._getForwardRates(curve) \
            * self._getDiscountFactors(curve) * self._accrualYearFractions
