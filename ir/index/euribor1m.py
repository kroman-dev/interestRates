from ir.scheduler.calendar.targetCalendar import TargetCalendar
from ir.scheduler.businessDayConvention.following import Following
from ir.dayCounter.act360 import Act360
from ir.index.index import Index


class Euribor1M(Index):

    def __init__(self):
        super().__init__(
            name='euribor1m',
            currency='EUR',
            tenor='1M',
            endOfMonth=False,
            businessDayConvention=Following(),
            dayCounter=Act360(),
            calendar=TargetCalendar()
        )
