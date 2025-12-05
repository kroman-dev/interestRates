from typing import Optional

from ir.curve.discountCurve import DiscountCurve
from ir.legs.genericLeg import GenericLeg


class Swap:

    def __init__(self, receiveLeg: GenericLeg, payLeg: GenericLeg):
        self._receiveLeg = receiveLeg
        self._payLeg = payLeg

    def npv(self, curve: Optional[DiscountCurve] = None) -> float:
        return self._receiveLeg.npv(curve) - self._payLeg.npv(curve)
