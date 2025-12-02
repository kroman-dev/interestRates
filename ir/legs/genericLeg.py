from abc import ABC, abstractmethod

import numpy as np

from ir.curve.discountCurve import DiscountCurve
from ir.dayCounter.genericDayCounter import GenericDayCounter
from ir.scheduler.businessDayConvention.genericBusinessDayConvention import \
    GenericBusinessDayConvention
from ir.scheduler.schedule.genericSchedule import GenericSchedule


class GenericLeg(ABC):

    def __init__(
            self,
            curve: DiscountCurve,
            schedule: GenericSchedule,
            businessDayConvention: GenericBusinessDayConvention,
            dayCounter: GenericDayCounter
    ):
        self._curve = curve
        self._schedule = schedule
        self._scheduleData = self._schedule.getSchedule()
        self._businessDayConvention = businessDayConvention
        self._dayCounter = dayCounter

        self._accrualYearFractions = [
            self._dayCounter.yearFraction(startDate=startDate, endDate=endDate)
            for startDate, endDate in zip(
                self._scheduleData.accrualStartDates,
                self._scheduleData.accrualEndDates
            )
        ]

    @abstractmethod
    def getCashFlows(self):
        pass

    def npv(self) -> float:
        return np.sum(self.getCashFlows())
