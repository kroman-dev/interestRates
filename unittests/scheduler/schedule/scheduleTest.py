from unittest import TestCase
from datetime import date

from ir.scheduler.businessDayConvention.following import Following
from ir.scheduler.calendar.russiaCalendar import RussiaCalendar
from ir.scheduler.schedule.schedule import Schedule
from ir.scheduler.stubPeriod.shortBack import ShortBack


class ScheduleTest(TestCase):

    def setUp(self):
        self._effectiveDate = date(2025, 11, 4)
        terminationDate = date(2025, 12, 4)
        frequency = '1M'
        businessDayConvention = Following()
        endOfMonth = False
        stubPeriod = ShortBack()
        calendar = RussiaCalendar()

        self._sampleSchedule = Schedule(
            effectiveDate=self._effectiveDate,
            terminationDate=terminationDate,
            frequency=frequency,
            businessDayConvention=businessDayConvention,
            endOfMonth=endOfMonth,
            stubPeriod=stubPeriod,
            calendar=calendar,
            paymentLag=1
        )

    def testGetSchedule(self):
        schedule = self._sampleSchedule.getSchedule()
        with self.subTest("start"):
            self.assertEqual(
                date(2025, 11, 5),
                schedule.accrualStartDates[0]
            )

        with self.subTest("end"):
            self.assertEqual(
                date(2025, 12, 4),
                schedule.accrualEndDates[0]
            )

        with self.subTest("payment"):
            self.assertEqual(
                date(2025, 12, 5),
                schedule.paymentDates[0]
            )
