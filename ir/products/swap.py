from typing import Optional

import numpy as np

from ir.curve.discountCurve import DiscountCurve
from ir.legs.genericLeg import GenericLeg


class Swap:

    def __init__(self, receiveLeg: GenericLeg, payLeg: GenericLeg):
        self._receiveLeg = receiveLeg
        self._payLeg = payLeg

    def npv(self, curve: Optional[DiscountCurve] = None) -> float:
        return self._receiveLeg.npv(curve) - self._payLeg.npv(curve)

    def getParRate(self, curve: Optional[DiscountCurve] = None) -> float:
        """
        The forward swap rate that RFS(fixRate) = 0
            Brigo ex. (1.25) p.15
        """
        return self._receiveLeg.npv(curve) / np.sum(
            self._payLeg._discountFactors * self._payLeg._accrualYearFractions
        ) / self._payLeg._notional

    def getFixRate(self) -> float:
        return self._payLeg.getFixRate()
