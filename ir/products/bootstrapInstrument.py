from abc import abstractmethod
from typing import Optional

from ir.curve.genericCurve import GenericCurve
from ir.products.instrument import Instrument


class BootstrapInstrument(Instrument):

    @abstractmethod
    def getParRate(self, curve: Optional[GenericCurve] = None) -> float:
        pass
