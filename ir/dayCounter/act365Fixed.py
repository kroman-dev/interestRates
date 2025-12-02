from datetime import date

from ir.dayCounter.genericDayCounter import GenericDayCounter


class Act365Fixed(GenericDayCounter):

    @classmethod
    def yearFraction(cls, startDate: date, endDate: date) -> float:
        return (endDate - startDate).days / 365
