from abc import ABC, abstractmethod

from ir.projectTyping.floatOrVectorType import FloatOrVectorType


class GenericInterpolator(ABC):

    @abstractmethod
    def _interpolate(self, x: FloatOrVectorType) -> FloatOrVectorType:
        pass

    def __call__(self, x: FloatOrVectorType) -> FloatOrVectorType:
        return self._interpolate(x)
