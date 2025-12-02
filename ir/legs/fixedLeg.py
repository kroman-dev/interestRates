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
            dayCounter: GenericDayCounter
    ):
        super().__init__(
            curve=curve,
            schedule=schedule,
            businessDayConvention=businessDayConvention,
            dayCounter=dayCounter
        )
        self._fixedRate = fixedRate

    def getCashFlows(self):
        cashFlows = []
        for periodIndex, accrual in enumerate(self._accrualYearFractions):
            cashFlows.append(
                self._curve.getDiscountFactor(
                    self._scheduleData.paymentDates[periodIndex]
                ) * accrual * self._fixedRate
            )
        return cashFlows

    def npv(self) -> float:
        return np.sum(self.getCashFlows())
