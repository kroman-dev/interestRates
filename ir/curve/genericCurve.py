from abc import ABC, abstractmethod
from datetime import date
from typing import List

from ir.curve.interpolator.genericInterpolator import GenericInterpolator
from ir.dayCounter.genericDayCounter import GenericDayCounter
from ir.dualNumbers.dualNumber import DualNumber
from ir.projectTyping.floatOrVectorType import FloatOrVectorType
from ir.projectTyping.floatVectorType import FloatVectorType


class GenericCurve(ABC):

    def __init__(
            self,
            dates: List[date],
            values: FloatVectorType,
            dayCounter: GenericDayCounter,
            interpolator: GenericInterpolator,
            enableExtrapolation: bool = False
    ):
        if len(dates) != len(values):
            raise ValueError('different length between dates and values')
        self._dates = dates
        self._values = values
        self._dayCounter = dayCounter
        self._interpolator = interpolator
        self._enableExtrapolation = enableExtrapolation

    def setEnableExtrapolation(self, enableExtrapolation: bool):
        self._enableExtrapolation = enableExtrapolation

    @abstractmethod
    def _interpolate(self, x: date) -> FloatOrVectorType:
        pass

    @abstractmethod
    def getDiscountFactor(self, x: date) -> FloatOrVectorType:
        pass

    def getForwardRate(self, periodStart: date, periodEnd: date) -> float:
        accrual = self._dayCounter.yearFraction(
            startDate=periodStart,
            endDate=periodEnd
        )

        return (
                self.getDiscountFactor(periodStart)
                / self.getDiscountFactor(periodEnd) - 1
        ) / accrual

    def setInterpolator(self, newInterpolator: GenericInterpolator):
        self._interpolator = newInterpolator

    def __call__(self, x: date) -> FloatOrVectorType:
        return self._interpolate(x)

    def __str__(self):
        output = (f"    DiscountCurve|{type(self._dayCounter).__qualname__}|"
                  f"{self._interpolator.__qualname__} \n")
        for _date, discountFactor in zip(self._dates, self._values):
            if isinstance(discountFactor, DualNumber):
                discountFactor = discountFactor.realPart
            output += f'{_date}: {discountFactor} \n'

        return output
