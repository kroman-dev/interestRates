from datetime import date
from typing import List

from ir.curve.genericCurve import GenericCurve
from ir.curve.interpolator.genericInterpolator import GenericInterpolator
from ir.curve.interpolator.logLinearInterpolator import LogLinearInterpolator
from ir.dayCounter.genericDayCounter import GenericDayCounter
from ir.projectTyping.floatOrVectorType import FloatOrVectorType
from ir.projectTyping.floatVectorType import FloatVectorType


class DiscountCurve(GenericCurve):

    def __init__(
            self,
            dates: List[date],
            discountFactors: FloatVectorType,
            dayCounter: GenericDayCounter,
            interpolator: GenericInterpolator = LogLinearInterpolator
    ):
        super().__init__(
            dates=dates,
            values=discountFactors,
            interpolator=interpolator,
        )
        self._dayCounter = dayCounter
        if (1. - discountFactors[0]) > 1e-15:
            raise Exception('First value must be 1.')
        self._curveDate = dates[0]

    def _interpolate(self, x: date) -> FloatOrVectorType:
        yearFraction = self._dayCounter.yearFraction(
            startDate=self._curveDate,
            endDate=x
        )
        if x < self._curveDate:
            raise ValueError('x before curveDate')
        if x > self._dates[-1]:
            raise ValueError('x in extrapolation domain')

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

    def __call__(self, x: date) -> FloatOrVectorType:
        return self._interpolate(x)
