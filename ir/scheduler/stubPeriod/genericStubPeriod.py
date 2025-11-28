from abc import ABC, abstractmethod
from datetime import date
from typing import List


class GenericStubPeriod(ABC):

    @staticmethod
    @abstractmethod
    def makeSchedule(
            startDate: date,
            endDate: date,
            frequency: str
    ) -> List[date]:
        pass
