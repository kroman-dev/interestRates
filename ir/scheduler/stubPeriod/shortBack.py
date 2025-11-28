from datetime import date
from typing import List

from ir.scheduler.period.period import Period
from ir.scheduler.stubPeriod.genericStubPeriod import GenericStubPeriod


class ShortBack(GenericStubPeriod):

    @staticmethod
    def makeSchedule(
            startDate: date,
            endDate: date,
            frequency: str
    ) -> List[date]:
        schedule = [startDate]
        referenceDate = startDate
        while endDate > referenceDate:
            referenceDate += Period(frequency)

            if endDate > referenceDate:
                schedule.append(referenceDate)

        schedule.append(endDate)

        return schedule
