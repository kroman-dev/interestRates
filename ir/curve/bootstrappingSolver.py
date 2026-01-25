from datetime import date
from typing import List, Dict, Tuple, Optional
from numpy.typing import NDArray

import numpy as np

from ir.curve.discountCurve import DiscountCurve
from ir.curve.genericCurve import GenericCurve
from ir.curve.interpolator.genericInterpolator import GenericInterpolator
from ir.curve.interpolator.logLinearInterpolator import LogLinearInterpolator
from ir.dayCounter.genericDayCounter import GenericDayCounter
from ir.dualNumbers.dualNumber import DualNumber
from ir.products.bootstrapInstrument import BootstrapInstrument


class BootstrappingSolver:

    def __init__(
            self,
            initialGuessNodes: Dict[date, float],
            instruments: List[BootstrapInstrument],
            instrumentsQuotes: List[float],
            dayCounter: GenericDayCounter,
            curveInterpolator: GenericInterpolator = LogLinearInterpolator,
            discountCurve: Optional[GenericCurve] = None
    ):
        """
            Note. In [1] discount factor are denoted as v_i, so in dual part
            I use keys v{index}
            [1] Darbyshire, Pricing and trading interest rate derivatives
        """
        if discountCurve is not None \
            and isinstance(
            discountCurve.getDiscountFactor(list(initialGuessNodes.keys())[0]),
            DualNumber
        ):
            raise ValueError(
                'Incorrect behavior for discountCurve with DualNumbers. '
                'Use discountCurve.convertToFloatValues()'
            )

        self._instruments = instruments
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
        self._instrumentsQuotes = np.array(instrumentsQuotes).transpose()

        self._bootstrappingStatus = 'unknown'
        self._regularizationParameter = 1000
        self._solverMethodName = "GaussNewton"

        self._discountCurve = discountCurve

        self._nodePointLength = len(list(self._initialGuessNodes.keys())) - 1
        if self._nodePointLength == len(instruments):
            self._bootstrappingStatus = 'completely specified curve'
        elif self._nodePointLength < len(instruments):
            self._bootstrappingStatus = 'overspecified curve'
        elif self._nodePointLength > len(instruments):
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
        discountCurve = curve if self._discountCurve is None \
            else self._discountCurve

        parRatesFromCurve = np.array([
            instrument.getParRate(
                discountCurve=discountCurve,
                forwardCurve=curve
            ) for instrument in self._instruments
        ]).transpose()

        difference = parRatesFromCurve - self._instrumentsQuotes

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

    @staticmethod
    def _updateStepGaussNewton(
            currentDiscountFactors: NDArray[DualNumber],
            gradientObjective: NDArray[DualNumber],
            jacobian: NDArray[DualNumber]
    ) -> NDArray[DualNumber]:
        # noinspection PyTypeChecker
        # Ax = b
        return currentDiscountFactors + np.linalg.solve(
            np.matmul(jacobian, jacobian.transpose()),
            - 0.5 * gradientObjective
        )

    def _updateStepLevenbergMarquardt(
            self,
            currentDiscountFactors: NDArray[DualNumber],
            gradientObjective: NDArray[DualNumber],
            jacobian: NDArray[DualNumber]
    ) -> NDArray[DualNumber]:
        # noinspection PyTypeChecker
        return currentDiscountFactors + np.linalg.solve(
            np.matmul(jacobian, jacobian.transpose())
            + self._regularizationParameter * np.eye(jacobian.shape[0]),
            - 0.5 * gradientObjective
        )

    @staticmethod
    def _treatSickCurve(curve: GenericCurve) -> GenericCurve:
        discountFactors = curve._values
        isTreated = False
        for index, discountFactor in enumerate(discountFactors):
            if (
                    isinstance(discountFactor, DualNumber)
                    and discountFactor.realPart <= 0
            ):
                discountFactors[index] = DualNumber(
                    1e-5,
                    discountFactor.dualPart
                )
                isTreated = True

        if isTreated:
            return DiscountCurve(
                dates=curve._dates,
                discountFactors=discountFactors,
                dayCounter=curve._dayCounter,
                interpolator=curve._interpolator,
                enableExtrapolation=curve._enableExtrapolation
            )
        return curve

    def _updateStep(
            self,
            curve: DiscountCurve,
            previousObjectiveValue: float
    ) -> Tuple[DualNumber, NDArray[DualNumber]]:
        curve = self._treatSickCurve(curve)
        currentDiscountFactors = np.array(curve._values[1:]).transpose()

        objectiveValue, gradientObjective, jacobian = \
            self._calculateMetrics(curve)

        if self._solverMethodName == "GaussNewton":
            return objectiveValue, self._updateStepGaussNewton(
                currentDiscountFactors=currentDiscountFactors,
                gradientObjective=gradientObjective,
                jacobian=jacobian
            )
        elif self._solverMethodName == "LevenbergMarquardt":
            self._regularizationParameter *= \
                2 if previousObjectiveValue < objectiveValue.realPart else 0.5
            return objectiveValue, self._updateStepLevenbergMarquardt(
                currentDiscountFactors=currentDiscountFactors,
                gradientObjective=gradientObjective,
                jacobian=jacobian
            )
        else:
            raise ValueError("unknown solver method")

    def solve(self) -> Tuple[DiscountCurve, bool]:
        maxIterations = 2000
        tolerance = 1e-16
        previousObjectiveValue = 1e10
        solutionCurve = self._initialDiscountCurve
        isSuccessConvergence = False
        for iterationIndex in range(maxIterations):
            objectiveValue, newDiscountFactors = \
                self._updateStep(
                    curve=solutionCurve,
                    previousObjectiveValue=previousObjectiveValue
                )
            if (objectiveValue.realPart < previousObjectiveValue) \
                and (
                    previousObjectiveValue - objectiveValue.realPart
            ) < tolerance:
                isSuccessConvergence = True
                break
            solutionCurve = self._buildNewCurve(newDiscountFactors)
            previousObjectiveValue = objectiveValue.realPart

        self._regularizationParameter = 1000
        return solutionCurve, isSuccessConvergence
