from ir.scheduler.calendar.targetCalendar import TargetCalendar
from ir.scheduler.businessDayConvention.following import Following
from ir.dayCounter.act360 import Act360
from ir.index.overnightIndex import OvernightIndex


class Eonia(OvernightIndex):

    def __init__(self):
        super().__init__(
            name='eonia',
            currency='EUR',
            endOfMonth=False,
            businessDayConvention=Following(),
            dayCounter=Act360(),
            calendar=TargetCalendar()
        )
