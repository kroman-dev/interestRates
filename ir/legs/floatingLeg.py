from typing import Optional

from ir.curve.discountCurve import DiscountCurve
from ir.dayCounter.genericDayCounter import GenericDayCounter
from ir.legs.genericLeg import GenericLeg
from ir.projectTyping.floatVectorType import FloatVectorType
from ir.scheduler.businessDayConvention.genericBusinessDayConvention import \
    GenericBusinessDayConvention
from ir.scheduler.schedule.genericSchedule import GenericSchedule


class FloatingLeg(GenericLeg):

    def __init__(
            self,
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
        self._forwardRates = self._getForwardRates(curve)

    def getCashFlows(
            self,
            curve: Optional[DiscountCurve] = None
    ) -> FloatVectorType:
        forwardRates = self._forwardRates
        discountFactors = self._discountFactors

        if curve is not None:
            forwardRates = self._getForwardRates(curve)
            discountFactors = self._getDiscountFactors(curve)

        return self._notional * forwardRates \
                    * discountFactors * self._accrualYearFractions
