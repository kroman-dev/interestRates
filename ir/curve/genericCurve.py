from abc import ABC, abstractmethod
from datetime import date
from typing import List

from ir.curve.interpolator.genericInterpolator import GenericInterpolator
from ir.projectTyping.floatOrVectorType import FloatOrVectorType
from ir.projectTyping.floatVectorType import FloatVectorType


class GenericCurve(ABC):

    def __init__(
            self,
            dates: List[date],
            values: FloatVectorType,
            interpolator: GenericInterpolator
    ):
        self._dates = dates
        self._values = values
        self._interpolator = interpolator

    @abstractmethod
    def _interpolate(self, x: date) -> FloatOrVectorType:
        pass

    @abstractmethod
    def getDiscountFactor(self, x: date) -> FloatOrVectorType:
        pass

    def setInterpolator(self, newInterpolator: GenericInterpolator):
        self._interpolator = newInterpolator

    def __call__(self, x: date) -> FloatOrVectorType:
        return self._interpolate(x)
