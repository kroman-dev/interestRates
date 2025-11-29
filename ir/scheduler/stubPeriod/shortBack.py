from datetime import date
from typing import List

from ir.scheduler.period.period import Period
from ir.scheduler.stubPeriod.genericStubPeriod import GenericStubPeriod
from ir.scheduler.stubPeriod.stubPeriodGenerationTypeEnum import \
    StubPeriodGenerationTypeEnum


class ShortBack(GenericStubPeriod):

    _stubPeriodGenerationType = StubPeriodGenerationTypeEnum("back")

    @classmethod
    def makeUnadjustedSchedule(
            cls,
            startDate: date,
            endDate: date,
            frequency: str
    ) -> List[date]:
        rawSchedule = [startDate]
        referenceDate = startDate
        while endDate > referenceDate:
            referenceDate += Period(frequency)

            if endDate > referenceDate:
                rawSchedule.append(referenceDate)

        rawSchedule.append(endDate)

        return rawSchedule
