from abc import ABC, abstractmethod
from datetime import date
from typing import List

from ir.scheduler.stubPeriod.stubPeriodGenerationTypeEnum import \
    StubPeriodGenerationTypeEnum


class GenericStubPeriod(ABC):

    _stubPeriodGenerationType: StubPeriodGenerationTypeEnum = None

    @staticmethod
    @abstractmethod
    def makeUnadjustedSchedule(
            startDate: date,
            endDate: date,
            frequency: str
    ) -> List[date]:
        pass

    @classmethod
    def getStubPeriodGenerationType(cls) -> StubPeriodGenerationTypeEnum:
        return cls._stubPeriodGenerationType
