from abc import ABC, abstractmethod
from typing import Optional

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
        self._discountFactors = self._getDiscountFactors(self._curve)

    def _getForwardRates(
            self,
            curve: Optional[DiscountCurve] = None
    ) -> FloatVectorType:
        return np.array([
            curve.getForwardRate(
                periodStart=startDate,
                periodEnd=endDate
            )
            for startDate, endDate in zip(
                self._scheduleData.accrualStartDates,
                self._scheduleData.accrualEndDates,
            )
        ])

    def _getDiscountFactors(self, curve: DiscountCurve) -> FloatVectorType:
        return np.array([
            curve.getDiscountFactor(paymentDate)
            for paymentDate in self._scheduleData.paymentDates
        ])

    @abstractmethod
    def getCashFlows(
            self,
            curve: Optional[DiscountCurve] = None
    ) -> FloatVectorType:
        pass

    def npv(self, curve: Optional[DiscountCurve] = None) -> float:
        return np.sum(self.getCashFlows(curve))
