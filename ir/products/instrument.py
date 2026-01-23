from abc import ABC, abstractmethod
from typing import Optional

from ir.curve.genericCurve import GenericCurve


class Instrument(ABC):

    @abstractmethod
    def npv(self, curve: Optional[GenericCurve] = None) -> float:
        pass
