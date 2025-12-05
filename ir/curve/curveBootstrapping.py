from datetime import date
from typing import List, Dict

from ir.curve.discountCurve import DiscountCurve
from ir.curve.interpolator.genericInterpolator import GenericInterpolator
from ir.curve.interpolator.logLinearInterpolator import LogLinearInterpolator
from ir.dayCounter.genericDayCounter import GenericDayCounter
from ir.dualNumbers.dualNumber import DualNumber
from ir.products.interestRateSwap import InterestRateSwap


class CurveBootstrapping:

    def __init__(
            self,
            initialGuessNodes: Dict[date, float],
            swaps: List[InterestRateSwap],
            dayCounter: GenericDayCounter,
            curveInterpolator: GenericInterpolator = LogLinearInterpolator
    ):
        self._swaps = swaps
        self._swapsRates = [swap.getFixRate() for swap in swaps]
        self._initialGuessNodes = initialGuessNodes
        self._curveInterpolator = curveInterpolator

        self._initialDiscountCurve = DiscountCurve(
            dates=list(initialGuessNodes.keys()),
            discountFactors=list(
                DualNumber(realPart=value, dualPart=f"v{index}")
                for index, value in enumerate(initialGuessNodes.values())
            ),
            dayCounter=dayCounter,
            interpolator=curveInterpolator
        )
        self._status = 'unknown'
        self._solverMethodName = "GaussNewton"
        if len(list(self._initialGuessNodes.keys()))  == len(swaps):
            self._status = 'completely specified curve'
        elif len(list(self._initialGuessNodes.keys()))  < len(swaps):
            self._status = 'overspecified curve'
        elif len(list(self._initialGuessNodes.keys()))  < len(swaps):
            self._status = 'underspecified curve'
            self._solverMethodName = "LevenbergMarquardt"
        else:
            raise ValueError('Cant specify curve')
