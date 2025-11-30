import numpy as np

from ir.curve.interpolator.genericInterpolator import GenericInterpolator
from ir.curve.interpolator.linearInterpolator import LinearInterpolator
from ir.projectTyping.floatOrVectorType import FloatOrVectorType


class LogLinearInterpolator(GenericInterpolator):

    def __init__(self, x1: float, x2: float, y1: float, y2: float):
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        self._linearInterpolator = LinearInterpolator(
            x1=self._x1,
            x2=self._x2,
            y1=np.log(self._y1),
            y2=np.log(self._y2)
        )

    def _interpolate(self, x: FloatOrVectorType) -> FloatOrVectorType:
        return np.exp(self._linearInterpolator(x))
