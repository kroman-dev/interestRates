from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import datetime


if TYPE_CHECKING:
    from ir.scheduler.calendar.genericCalendar import GenericCalendar


class GenericBusinessDayConvention(ABC):

    """
        A business day convention is a convention for adjustment of dates when
         a specified date is not a good business day. The adjustment is done
         with respect to a specific calendar. [1]

         Ref:
         [1]  OpenGamma, Interest Rate Instruments and Market Conventions Guide
    """

    @staticmethod
    @abstractmethod
    def adjust(
            date: datetime.date,
            calendar: 'GenericCalendar'
    ) -> datetime.date:
        pass
