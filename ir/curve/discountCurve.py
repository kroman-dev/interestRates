from datetime import date
from typing import List, Union

from ir.curve.genericCurve import GenericCurve
from ir.curve.interpolator.genericInterpolator import GenericInterpolator
from ir.curve.interpolator.logLinearInterpolator import LogLinearInterpolator
from ir.dayCounter.genericDayCounter import GenericDayCounter
from ir.dualNumbers.dualNumber import DualNumber
from ir.projectTyping.floatOrVectorType import FloatOrVectorType
from ir.projectTyping.floatVectorType import FloatVectorType


class DiscountCurve(GenericCurve):

    def __init__(
            self,
            dates: List[date],
            discountFactors: Union[List[DualNumber], FloatVectorType],
            dayCounter: GenericDayCounter,
            interpolator: GenericInterpolator = LogLinearInterpolator,
            enableExtrapolation: bool = False
    ):
        super().__init__(
            dates=dates,
            values=discountFactors,
            dayCounter=dayCounter,
            interpolator=interpolator,
            enableExtrapolation=enableExtrapolation
        )
        if isinstance(discountFactors[0], DualNumber):
            if (1. - discountFactors[0].realPart) > 1e-15:
                raise Exception('First value must be 1.')
        elif (1. - discountFactors[0]) > 1e-15:
            raise Exception('First value must be 1.')
        self._curveDate = dates[0]

    def convertToFloatValues(self):
        return DiscountCurve(
            dates=self._dates,
            discountFactors=[value.realPart for value in self._values],
            dayCounter=self._dayCounter,
            interpolator=self._interpolator,
            enableExtrapolation=self._enableExtrapolation
        )

    def _interpolate(self, x: date) -> FloatOrVectorType:
        yearFraction = self._dayCounter.yearFraction(
            startDate=self._curveDate,
            endDate=x
        )
        if x < self._curveDate:
            raise ValueError('x before curveDate')
        if x > self._dates[-1]:
            if not self._enableExtrapolation:
                raise ValueError('x in extrapolation domain')
            # noinspection PyCallingNonCallable
            return self._interpolator(
                x1=self._dayCounter.yearFraction(
                    startDate=self._curveDate,
                    endDate=self._dates[-2]
                ),
                x2=self._dayCounter.yearFraction(
                    startDate=self._curveDate,
                    endDate=self._dates[-1]
                ),
                y1=self._values[-2],
                y2=self._values[-1]
            )(yearFraction)

        for intervalIndex, (startDate, endDate) in enumerate(
                zip(self._dates[:-1], self._dates[1:])
        ):
            if (startDate <= x) and (x <= endDate):
                # noinspection PyCallingNonCallable
                return self._interpolator(
                    x1=self._dayCounter.yearFraction(
                        startDate=self._curveDate,
                        endDate=startDate
                    ),
                    x2=self._dayCounter.yearFraction(
                        startDate=self._curveDate,
                        endDate=endDate
                    ),
                    y1=self._values[intervalIndex],
                    y2=self._values[intervalIndex + 1]
                )(yearFraction)

        raise Exception('incorrect input')

    def getDiscountFactor(self, x: date) -> FloatOrVectorType:
        return self._interpolate(x)
