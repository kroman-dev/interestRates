import numpy

from abc import ABC, abstractmethod
from typing import Optional

from ir.curve.genericCurve import GenericCurve
from ir.dualNumbers.dualNumber import DualNumber
from ir.projectTyping.floatVectorType import FloatVectorType


class Instrument(ABC):

    @abstractmethod
    def npv(
            self,
            discountCurve: Optional[GenericCurve] = None,
            forwardCurve: Optional[GenericCurve] = None
    ) -> float:
        pass

    def getDeltas(
            self,
            discountCurve: Optional[GenericCurve] = None,
            forwardCurve: Optional[GenericCurve] = None
    ) -> FloatVectorType:
        if not isinstance(discountCurve._values[-1], DualNumber):
            raise ValueError('Use DualNumber with discountCurve')
        # TODO forwardCurve?
        dualNpv: DualNumber = \
            self.npv(discountCurve=discountCurve, forwardCurve=forwardCurve)

        if len(list(dualNpv.dualPart.keys())) != discountCurve.getJacobian().shape[-1]:

            npvDualComponentsNames = [
                int(dualName.split('v')[-1])
                for dualName in dualNpv.dualPart.keys()
            ]

            dualNpv = DualNumber(
                realPart=dualNpv.realPart,
                dualPart={
                    f'v{dualPartIndex}': 0.
                    if dualPartIndex not in npvDualComponentsNames
                    else dualNpv.dualPart.get(f'v{dualPartIndex}')
                    for dualPartIndex in range(max(npvDualComponentsNames) + 1)
                }
            )

        return numpy.matmul(
            discountCurve.getJacobian(),
            numpy.array(list(dualNpv.dualPart.values()))[None].transpose()
        )
