from abc import ABC

from ir.scheduler.schedule.genericSchedule import GenericSchedule


class GenericLeg(ABC):

    def __init__(
            self,
            schedule: GenericSchedule,
    ):
        pass
