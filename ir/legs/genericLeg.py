from abc import ABC, abstractmethod

import numpy as np

from ir.curve.discountCurve import DiscountCurve
from ir.dayCounter.genericDayCounter import GenericDayCounter
from ir.projectTyping.floatVectorType import FloatVectorType
from ir.scheduler.businessDayConvention.genericBusinessDayConvention import \
    GenericBusinessDayConvention
from ir.scheduler.schedule.genericSchedule import GenericSchedule


class GenericLeg(ABC):

    def __init__(
            self,
            curve: DiscountCurve,
            schedule: GenericSchedule,
            businessDayConvention: GenericBusinessDayConvention,
            dayCounter: GenericDayCounter,
            notional: float,
    ):
        self._curve = curve
        self._schedule = schedule
        self._scheduleData = self._schedule.getSchedule()
        self._businessDayConvention = businessDayConvention
        self._dayCounter = dayCounter
        self._notional = notional

        self._accrualYearFractions = np.array([
            self._dayCounter.yearFraction(startDate=startDate, endDate=endDate)
            for startDate, endDate in zip(
                self._scheduleData.accrualStartDates,
                self._scheduleData.accrualEndDates
            )
        ])
        self._discountFactors = np.array([
            self._curve.getDiscountFactor(paymentDate)
            for paymentDate in self._scheduleData.paymentDates
        ])

    @abstractmethod
    def getCashFlows(self) -> FloatVectorType:
        pass

    def npv(self) -> float:
        return np.sum(self.getCashFlows())
