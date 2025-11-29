from abc import ABC, abstractmethod
from datetime import date


class GenericDayCounter(ABC):

    @classmethod
    @abstractmethod
    def yearFraction(cls, startDate: date, endDate: date) -> float:
        pass
