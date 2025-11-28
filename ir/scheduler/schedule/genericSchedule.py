from datetime import date
from abc import ABC, abstractmethod

from ir.scheduler.businessDayConvention.businessDayConvention import \
    BusinessDayConvention


class GenericSchedule(ABC):

    @abstractmethod
    def getSchedule(
            self,
            effectiveDate: date,
            terminationDate: date,
            frequency: str,
            businessDayConvention: BusinessDayConvention,
            endOfMonth: bool
    ):
        pass
