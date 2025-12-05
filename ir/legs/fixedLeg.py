import numpy as np

from ir.curve.discountCurve import DiscountCurve
from ir.legs.genericLeg import GenericLeg
from ir.dayCounter.genericDayCounter import GenericDayCounter
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

    def getCashFlows(self):
        cashFlows = []

        # self._notional * self._fixedRate * np.
        for periodIndex, accrual in enumerate(self._accrualYearFractions):
            cashFlows.append(
                self._curve.getDiscountFactor(
                    self._scheduleData.paymentDates[periodIndex]
                ) * accrual * self._fixedRate
            )
        return cashFlows
