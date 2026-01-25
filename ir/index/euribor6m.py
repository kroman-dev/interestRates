from ir.scheduler.calendar.targetCalendar import TargetCalendar
from ir.scheduler.businessDayConvention.modifiedFollowing import ModifiedFollowing
from ir.dayCounter.act360 import Act360
from ir.index.index import Index


class Euribor6M(Index):

    def __init__(self):
        super().__init__(
            name='euribor6m',
            currency='EUR',
            tenor='6M',
            endOfMonth=False,
            businessDayConvention=ModifiedFollowing(),
            dayCounter=Act360(),
            calendar=TargetCalendar()
        )
