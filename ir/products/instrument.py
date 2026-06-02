from abc import ABC, abstractmethod
from typing import Optional

import numpy

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
        # TODO multicurve?
        npv: DualNumber = \
            self.npv(discountCurve=discountCurve, forwardCurve=forwardCurve)

        if len(list(npv.dualPart.keys())) != discountCurve.getJacobian().shape[-1]:
            npvDualComponentsNames = [
                int(dualName.split('v')[-1])
                for dualName in npv.dualPart.keys()
            ]
            # correcting npv dual part with zero values for missing components
            npv = DualNumber(
                realPart=npv.realPart,
                dualPart={
                    f'v{dualPartIndex}': 0.
                    if dualPartIndex not in npvDualComponentsNames
                    else npv.dualPart.get(f'v{dualPartIndex}')
                    for dualPartIndex in range(
                        discountCurve.getJacobian().shape[-1]
                    )
                }
            )

        # TODO sth strange in scaling
        return numpy.matmul(
            discountCurve.getJacobian(),
            numpy.array(list(npv.dualPart.values()))[None].transpose()
        )
