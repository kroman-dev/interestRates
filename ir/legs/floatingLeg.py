from ir.curve.discountCurve import DiscountCurve
from ir.dayCounter.genericDayCounter import GenericDayCounter
from ir.legs.genericLeg import GenericLeg
from ir.scheduler.businessDayConvention.genericBusinessDayConvention import \
    GenericBusinessDayConvention
from ir.scheduler.schedule.genericSchedule import GenericSchedule


class FloatingLeg(GenericLeg):

    def __init__(
            self,
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

    def getCashFlows(self):
        cashFlows = []

        for startDate, endDate, paymentDate, accrual in zip(
                self._scheduleData.accrualStartDates,
                self._scheduleData.accrualEndDates,
                self._scheduleData.paymentDates,
                self._accrualYearFractions
        ):
            cashFlows.append(
                self._curve.getDiscountFactor(paymentDate) \
                * accrual * self._curve.getForwardRate(
                    periodStart=startDate,
                    periodEnd=endDate
                )
            )
        return cashFlows
