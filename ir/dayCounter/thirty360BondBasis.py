from datetime import date

from ir.dayCounter.genericThirty360 import GenericThirty360


class Thirty360BondBasis(GenericThirty360):

    """
        30/360
    """

    @classmethod
    def yearFraction(cls, startDate: date, endDate: date) -> float:
        day1 = 30 if startDate.day == 31 else startDate.day
        day2 = 30 if endDate.day == 31 and day1 == 30 else endDate.day
        month1 = startDate.month
        month2 = endDate.month
        year1 = startDate.year
        year2 = endDate.year

        return cls._baseYearFraction30360(
            day1=day1,
            day2=day2,
            month1=month1,
            month2=month2,
            year1=year1,
            year2=year2
        )
