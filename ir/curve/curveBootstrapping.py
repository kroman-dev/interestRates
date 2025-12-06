from datetime import date
from typing import List, Dict, Tuple
from numpy.typing import NDArray

import numpy as np

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
        """
            Note. In [1] discount factor are denoted as v_i, so in dual part
            I use keys v{index}
            [1] Darbyshire, Pricing and trading interest rate derivatives
        """
        self._swaps = swaps
        self._swapsRates = [swap.getFixRate() for swap in swaps]
        self._initialGuessNodes = initialGuessNodes
        self._curveInterpolator = curveInterpolator
        self._curveDates = list(initialGuessNodes.keys())
        self._curveDayCounter = dayCounter

        self._initialDiscountCurve = DiscountCurve(
            dates=self._curveDates,
            discountFactors=list(
                DualNumber(realPart=value, dualPart={f"v{index}": 1})
                for index, value in enumerate(initialGuessNodes.values())
            ),
            dayCounter=self._curveDayCounter,
            interpolator=self._curveInterpolator
        )
        self._swapsParRates = np.array([
            swap.getFixRate() for swap in self._swaps
        ]).transpose()

        self._bootstrappingStatus = 'unknown'
        self._solverMethodName = "GaussNewton"

        self._nodePointLength = len(list(self._initialGuessNodes.keys())) - 1
        if self._nodePointLength == len(swaps):
            self._bootstrappingStatus = 'completely specified curve'
        elif self._nodePointLength < len(swaps):
            self._bootstrappingStatus = 'overspecified curve'
        elif self._nodePointLength < len(swaps):
            self._bootstrappingStatus = 'underspecified curve'
            self._solverMethodName = "LevenbergMarquardt"
        else:
            raise ValueError('Cant specify curve')

    def _buildNewCurve(
            self,
            discountFactors: NDArray[DualNumber]
    ) -> DiscountCurve:
        return DiscountCurve(
            dates=self._curveDates,
            discountFactors=np.concatenate([
                np.array([DualNumber(realPart=1., dualPart={'v0': 1})]),
                discountFactors
            ]),
            dayCounter=self._curveDayCounter,
            interpolator=self._curveInterpolator
        )

    def _calculateMetrics(self, curve: DiscountCurve):
        parRatesFromCurve = np.array([
            swap.getParRate(curve) for swap in self._swaps
        ]).transpose()

        difference = parRatesFromCurve - self._swapsParRates

        objectiveValue = np.matmul(difference.transpose(), difference)
        gradientObjective = np.array(
            list(objectiveValue.dualPart.values())[1:]
        ).transpose()
        jacobian = np.array([
            [
                parRate.dualPart.get(f'v{index + 1}', 0)
                for parRate in parRatesFromCurve
            ]
            for index in range(self._nodePointLength)
        ])
        return objectiveValue, gradientObjective, jacobian

    def _updateStepGaussNewton(
            self,
            curve: DiscountCurve
    ) -> Tuple[DualNumber, NDArray[DualNumber]]:
        currentDiscountFactors = np.array(curve._values[1:]).transpose()
        objectiveValue, gradientObjective, jacobian = \
            self._calculateMetrics(curve)
        # Ax = b
        return objectiveValue, currentDiscountFactors + np.linalg.solve(
            np.matmul(jacobian, jacobian.transpose()),
            - 0.5 * gradientObjective
        )

    def _updateStep(
            self,
            curve: DiscountCurve
    ) -> Tuple[DualNumber, NDArray[DualNumber]]:
        if self._solverMethodName == "GaussNewton":
            return self._updateStepGaussNewton(curve)
        elif self._solverMethodName == "LevenbergMarquardt":
            return self._updateStepLevenbergMarquardt(curve)
        else:
            raise ValueError("unknown solver method")

    def solve(self) -> Tuple[DiscountCurve, bool]:
        maxIterations = 100
        tolerance = 1e-10
        previousObjectiveValue = 1e10
        solutionCurve = self._initialDiscountCurve
        isSuccessConvergence = False
        for iterationIndex in range(maxIterations):
            objectiveValue, newDiscountFactors = \
                self._updateStep(solutionCurve)
            if (
                    (objectiveValue.realPart < previousObjectiveValue)
                    and (
                        previousObjectiveValue - objectiveValue.realPart
                    ) < tolerance
            ):
                isSuccessConvergence = True
                break
            # TODO add LevenbergMarquardt
            solutionCurve = self._buildNewCurve(newDiscountFactors)
            previousObjectiveValue = objectiveValue.realPart

        return solutionCurve, isSuccessConvergence
