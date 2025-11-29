from datetime import date
from typing import List

from ir.scheduler.period.period import Period
from ir.scheduler.stubPeriod.genericStubPeriod import GenericStubPeriod
from ir.scheduler.stubPeriod.stubPeriodGenerationTypeEnum import \
    StubPeriodGenerationTypeEnum


class ShortFront(GenericStubPeriod):

    _stubPeriodGenerationType = StubPeriodGenerationTypeEnum('front')

    @classmethod
    def makeUnadjustedSchedule(
            cls,
            startDate: date,
            endDate: date,
            frequency: str
    ) -> List[date]:
        rawSchedule = [endDate]
        referenceDate = endDate
        while referenceDate > startDate:
            referenceDate -= Period(frequency)

            if referenceDate > startDate:
                rawSchedule.append(referenceDate)

        rawSchedule.append(startDate)

        return rawSchedule[::-1]
