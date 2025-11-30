from ir.curve.interpolator.genericInterpolator import GenericInterpolator
from ir.projectTyping.floatOrVectorType import FloatOrVectorType


class LinearInterpolator(GenericInterpolator):

    def __init__(self, x1: float, x2: float, y1: float, y2: float):
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2

    def _interpolate(self, x: FloatOrVectorType) -> FloatOrVectorType:
        return self._y1 + (x - self._x1) * (self._y2 - self._y1) \
            / (self._x2 - self._x1)
