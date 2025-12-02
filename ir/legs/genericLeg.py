from abc import ABC, abstractmethod

from ir.curve.discountCurve import DiscountCurve
from ir.dayCounter.genericDayCounter import GenericDayCounter
from ir.scheduler.businessDayConvention.genericBusinessDayConvention import \
    GenericBusinessDayConvention
from ir.scheduler.schedule.genericSchedule import GenericSchedule


class GenericLeg(ABC):

    def __init__(
            self,
            curve: DiscountCurve,
            schedule: GenericSchedule,
            businessDayConvention: GenericBusinessDayConvention,
            dayCounter: GenericDayCounter
    ):
        self._schedule = schedule
        self._scheduleData = self._schedule.getSchedule()
        self._businessDayConvention = businessDayConvention
        self._dayCounter = dayCounter

    @abstractmethod
    def getCashFlows(self):
        pass

    @abstractmethod
    def npv(self) -> float:
        pass
