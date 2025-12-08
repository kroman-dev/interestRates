from datetime import date

from ir.dayCounter.genericDayCounter import GenericDayCounter


class Act360(GenericDayCounter):

    @classmethod
    def yearFraction(cls, startDate: date, endDate: date) -> float:
        return (endDate - startDate).days / 360
