from datetime import date

from ir.dayCounter.act365Fixed import Act365Fixed
from ir.scheduler.businessDayConvention.noConvention import NoConvention
from ir.scheduler.calendar.noCalendar import NoCalendar
from ir.scheduler.schedule.schedule import Schedule
from ir.scheduler.stubPeriod.shortBack import ShortBack


if __name__ == '__main__':
    schedule = Schedule(
        effectiveDate=date(2022, 1, 1),
        terminationDate=date(2022, 12, 1),
        frequency='3M',
        businessDayConvention=NoConvention,
        endOfMonth=False,
        stubPeriod=ShortBack,
        calendar=NoCalendar()
    ).getSchedule()

    for startDate, endDate in zip(
            schedule.accrualStartDates,
            schedule.accrualEndDates
    ):
        print(Act365Fixed().yearFraction(startDate=startDate, endDate=endDate))
