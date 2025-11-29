from ir.dayCounter.genericDayCounter import GenericDayCounter


class GenericThirty360(GenericDayCounter):

    @staticmethod
    def _baseYearFraction30360(
            day1: int,
            day2: int,
            month1: int,
            month2: int,
            year1: int,
            year2: int
    ):
        return (
                360 * (year2 - year1) + 30 * (month2 - month1) + (day2 - day1)
        ) / 360
