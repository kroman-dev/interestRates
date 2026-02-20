from abc import ABC, abstractmethod
from typing import Optional

import numpy as np

from ir.curve.genericCurve import GenericCurve
from ir.dayCounter.genericDayCounter import GenericDayCounter
from ir.projectTyping.floatVectorType import FloatVectorType
from ir.scheduler.schedule.genericSchedule import GenericSchedule


class GenericLeg(ABC):

    def __init__(
            self,
            schedule: GenericSchedule,
            dayCounter: GenericDayCounter,
            notional: float,
            discountCurve: Optional[GenericCurve] = None,
            forwardCurve: Optional[GenericCurve] = None
    ):
        self._discountCurve = discountCurve
        self._forwardCurve = forwardCurve
        self._schedule = schedule
        self._scheduleData = self._schedule.getSchedule()
        self._dayCounter = dayCounter
        self._notional = notional

        self._accrualYearFractions = np.array([
            self._dayCounter.yearFraction(startDate=startDate, endDate=endDate)
            for startDate, endDate in zip(
                self._scheduleData.accrualStartDates,
                self._scheduleData.accrualEndDates
            )
        ])

    def getDiscountCurve(self) -> Optional[GenericCurve]:
        return self._discountCurve

    def getForwardCurve(self) -> Optional[GenericCurve]:
        return self._forwardCurve

    def getNotional(self) -> float:
        return self._notional

    def getSchedule(self) -> GenericSchedule:
        return self._schedule

    def getAccruals(self) -> FloatVectorType:
        return self._accrualYearFractions

    def getForwardRates(
            self,
            curve: Optional[GenericCurve] = None
    ) -> FloatVectorType:
        forwardCurve = curve if curve is not None else self._forwardCurve
        if forwardCurve is None:
            if self._discountCurve is None:
                raise ValueError('there is no curve to calculate')
            else:
                forwardCurve = self._discountCurve

        return np.array([
            forwardCurve.getForwardRate(
                periodStart=startDate,
                periodEnd=endDate
            )
            for startDate, endDate in zip(
                self._scheduleData.accrualStartDates,
                self._scheduleData.accrualEndDates,
            )
        ])

    def getDiscountFactors(
            self,
            curve: Optional[GenericCurve] = None
    ) -> FloatVectorType:
        discountCurve = self._discountCurve if curve is None else curve
        return np.array([
            discountCurve.getDiscountFactor(paymentDate)
            for paymentDate in self._scheduleData.paymentDates
        ])

    def setDiscountCurve(self, curve: GenericCurve):
        self._discountCurve = curve

    def setForwardCurve(self, curve: GenericCurve):
        self._forwardCurve = curve

    @abstractmethod
    def getCashFlows(
            self,
            discountCurve: Optional[GenericCurve] = None,
            forwardCurve: Optional[GenericCurve] = None
    ) -> FloatVectorType:
        pass

    def npv(
            self,
            discountCurve: Optional[GenericCurve] = None,
            forwardCurve: Optional[GenericCurve] = None
    ) -> float:
        return np.sum(
            self.getCashFlows(
                discountCurve=discountCurve,
                forwardCurve=forwardCurve
            )
        )
