from datetime import date
from typing import List

from ir.scheduler.period.period import Period
from ir.scheduler.stubPeriod.genericStubPeriod import GenericStubPeriod


class ShortFront(GenericStubPeriod):

    @staticmethod
    def makeSchedule(
            startDate: date,
            endDate: date,
            frequency: str
    ) -> List[date]:
        schedule = [endDate]
        referenceDate = endDate
        while referenceDate > startDate:
            referenceDate -= Period(frequency)

            if referenceDate > startDate:
                schedule.append(referenceDate)

        schedule.append(startDate)

        return schedule[::-1]
