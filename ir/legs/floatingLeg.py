import numpy as np

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
        self._forwardRates = np.array([
            self._curve.getForwardRate(
                periodStart=startDate,
                periodEnd=endDate
            )
            for startDate, endDate in zip(
                self._scheduleData.accrualStartDates,
                self._scheduleData.accrualEndDates,
            )
        ])


    def getCashFlows(self) -> FloatVectorType:
        return self._notional * self._forwardRates \
                    * self._discountFactors * self._accrualYearFractions
