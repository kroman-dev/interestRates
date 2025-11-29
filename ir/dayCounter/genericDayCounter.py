from abc import ABC, abstractmethod


class GenericDayCounter(ABC):

    @staticmethod
    @abstractmethod
    def yearFraction(startDate, endDate):
        pass
