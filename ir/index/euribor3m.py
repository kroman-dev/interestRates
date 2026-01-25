from ir.scheduler.calendar.targetCalendar import TargetCalendar
from ir.scheduler.businessDayConvention.modifiedFollowing import ModifiedFollowing
from ir.dayCounter.act360 import Act360
from ir.index.index import Index


class Euribor3M(Index):

    def __init__(self):
        super().__init__(
            name='euribor3m',
            currency='EUR',
            tenor='3M',
            endOfMonth=False,
            businessDayConvention=ModifiedFollowing(),
            dayCounter=Act360(),
            calendar=TargetCalendar()
        )
