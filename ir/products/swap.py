from typing import Optional

import numpy as np

from ir.curve.genericCurve import GenericCurve
from ir.legs.genericLeg import GenericLeg
from ir.products.bootstrapInstrument import BootstrapInstrument


class Swap(BootstrapInstrument):

    def __init__(self, receiveLeg: GenericLeg, payLeg: GenericLeg):
        self._receiveLeg = receiveLeg
        self._payLeg = payLeg

    def __str__(self):
        frequency = self._receiveLeg._schedule._frequency
        terminationDate = self._receiveLeg._schedule._terminationDate
        effectiveDate = self._receiveLeg._schedule._effectiveDate
        return f"{effectiveDate}_{frequency}_{terminationDate}"

    def npv(self, curve: Optional[GenericCurve] = None) -> float:
        return self._receiveLeg.npv(curve) - self._payLeg.npv(curve)

    def getParRate(self, curve: Optional[GenericCurve] = None) -> float:
        """
        The forward swap rate that RFS(fixRate) = 0
            Brigo ex. (1.25) p.15
        """
        discountCurve = curve if self._receiveLeg.getDiscountCurve() is None \
            else self._receiveLeg.getDiscountCurve()

        return self._receiveLeg.npv(curve) / np.sum(
            self._payLeg.getDiscountFactors(discountCurve)
            * self._payLeg.getAccruals()
        ) / self._payLeg.getNotional()
