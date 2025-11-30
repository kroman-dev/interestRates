from abc import ABC, abstractmethod
from datetime import date
from typing import List

from ir.curve.interpolator.genericInterpolator import GenericInterpolator


class GenericCurve(ABC):

    def __init__(
            self,
            dates: List[date],
            values: List[float],
            interpolator: GenericInterpolator
    ):
        self._dates = dates
        self._values = values
        self._interpolator = interpolator

    def setInterpolator(self, newInterpolator: GenericInterpolator):
        self._interpolator = newInterpolator

    @abstractmethod
    def __call__(self, x: date) -> float:
        pass
