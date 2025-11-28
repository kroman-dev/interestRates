from dataclasses import dataclass
from typing import List
from datetime import date
from pandas import DataFrame


@dataclass
class ScheduleData:
    accrualStartDates: List[date]
    accrualEndDates: List[date]
    paymentDates: List[date]

    def __repr__(self):
        result = DataFrame()
        result['accrualStartDates'] = self.accrualStartDates
        result['accrualEndDates'] = self.accrualEndDates
        result['paymentDates'] = self.paymentDates
        return result.__repr__()
