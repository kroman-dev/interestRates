from datetime import date

from ir.scheduler.schedule.scheduleData import ScheduleData


if __name__ == '__main__':
    scheduleData = ScheduleData(
        accrualStartDates=[date(2025, 1, 1), date(2025, 2, 1)],
        accrualEndDates=[date(2025, 2, 1), date(2025, 3, 1)],
        paymentDates=[date(2025, 2, 1), date(2025, 3, 1)]
    )

    print(scheduleData)
