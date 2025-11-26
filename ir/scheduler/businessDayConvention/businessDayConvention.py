from abc import ABC, abstractmethod

import datetime


class BusinessDayConvention(ABC):

    """
        A business day convention is a convention for adjustment of dates when
         a specified date is not a good business day. The adjustment is done
         with respect to a specific calendar. [1]

         Ref:
         [1]  OpenGamma, Interest Rate Instruments and Market Conventions Guide
    """

    @staticmethod
    @abstractmethod
    def adjust(date: datetime.date) -> datetime.date:
        pass
