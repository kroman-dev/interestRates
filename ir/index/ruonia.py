from ir.scheduler.calendar.russiaCalendar import RussiaCalendar
from ir.scheduler.businessDayConvention.modifiedFollowing \
    import ModifiedFollowing
from ir.dayCounter.act365Fixed import Act365Fixed
from ir.index.overnightIndex import OvernightIndex


class Ruonia(OvernightIndex):

    def __init__(self):
        super().__init__(
            name='ruonia',
            currency='RUB',
            endOfMonth=False,
            businessDayConvention=ModifiedFollowing(),
            dayCounter=Act365Fixed(),
            calendar=RussiaCalendar()
        )
