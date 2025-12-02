from ir.legs.genericLeg import GenericLeg
from ir.dayCounter.genericDayCounter import GenericDayCounter
from ir.scheduler.businessDayConvention.genericBusinessDayConvention import \
    GenericBusinessDayConvention
from ir.scheduler.schedule.genericSchedule import GenericSchedule


class FixedLeg(GenericLeg):

    def __init__(
            self,
            schedule: GenericSchedule,
            businessDayConvention: GenericBusinessDayConvention,
            dayCounter: GenericDayCounter
    ):
        super().__init__(
            schedule=schedule,
            businessDayConvention=businessDayConvention,
            dayCounter=dayCounter
        )

        accrualYearFractions = [
            self._dayCounter.yearFraction(startDate=startDate, endDate=endDate)
            for startDate, endDate in zip(
                self._scheduleData.accrualStartDates,
                self._scheduleData.accrualEndDates
            )
        ]
        paymentYearFractions = [
            self._dayCounter.yearFraction(startDate=startDate, endDate=endDate)
            for startDate, endDate in zip(
                self._scheduleData.accrualStartDates,
                self._scheduleData.paymentDates
            )
        ]

    def getCashFlows(self):
        pass

    def npv(self) -> float:
        pass
