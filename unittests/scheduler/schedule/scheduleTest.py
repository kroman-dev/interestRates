from unittest import TestCase
from datetime import date

from ir.scheduler.businessDayConvention.following import Following
from ir.scheduler.calendar.russiaCalendar import RussiaCalendar
from ir.scheduler.schedule.schedule import Schedule
from ir.scheduler.stubPeriod.shortBack import ShortBack
from ir.scheduler.stubPeriod.shortFront import ShortFront


class ScheduleTest(TestCase):

    def testGetScheduleFront(self):
        sampleSchedule = Schedule(
            effectiveDate=date(2025, 2, 28),
            terminationDate=date(2025, 6, 3),
            frequency='1M',
            businessDayConvention=Following(),
            endOfMonth=True,
            stubPeriod=ShortFront(),
            calendar=RussiaCalendar(),
            paymentLag=0
        )
        schedule = sampleSchedule.getSchedule()

        with self.subTest("start dates"):
            self.assertListEqual(
                [
                    date(2025, 2, 28),
                    date(2025, 3, 3),
                    date(2025, 4, 3),
                    date(2025, 5, 5)
                ],
                schedule.accrualStartDates
            )

        with self.subTest("end dates"):
            self.assertListEqual(
                [
                    date(2025, 3, 3),
                    date(2025, 4, 3),
                    date(2025, 5, 5),
                    date(2025, 6, 3)
                ],
                schedule.accrualEndDates
            )

    def testGetScheduleWorkingEomFront(self):
        sampleSchedule = Schedule(
            effectiveDate=date(2025, 2, 28),
            terminationDate=date(2025, 6, 30),
            frequency='1M',
            businessDayConvention=Following(),
            endOfMonth=True,
            stubPeriod=ShortFront(),
            calendar=RussiaCalendar(),
            paymentLag=0
        )
        schedule = sampleSchedule.getSchedule()

        with self.subTest("start dates"):
            self.assertListEqual(
                [
                    date(2025, 2, 28),
                    date(2025, 3, 31),
                    date(2025, 4, 30),
                    date(2025, 5, 30)
                ],
                schedule.accrualStartDates
            )

        with self.subTest("end dates"):
            self.assertListEqual(
                [
                    date(2025, 3, 31),
                    date(2025, 4, 30),
                    date(2025, 5, 30),
                    date(2025, 6, 30)
                ],
                schedule.accrualEndDates
            )

    def testGetScheduleNotWorkingEomBack(self):
        sampleSchedule = Schedule(
            effectiveDate=date(2025, 1, 28),
            terminationDate=date(2025, 6, 3),
            frequency='1M',
            businessDayConvention=Following(),
            endOfMonth=True,
            stubPeriod=ShortBack(),
            calendar=RussiaCalendar(),
            paymentLag=0
        )
        schedule = sampleSchedule.getSchedule()

        with self.subTest("start dates"):
            self.assertListEqual(
                [
                    date(2025, 1, 28),
                    date(2025, 2, 28),
                    date(2025, 3, 28),
                    date(2025, 4, 28),
                    date(2025, 5, 28)
                ],
                schedule.accrualStartDates
            )

        with self.subTest("end dates"):
            self.assertListEqual(
                [
                    date(2025, 2, 28),
                    date(2025, 3, 28),
                    date(2025, 4, 28),
                    date(2025, 5, 28),
                    date(2025, 6, 3)
                ],
                schedule.accrualEndDates
            )

    def testGetScheduleWithWorkingEomBack(self):
        sampleSchedule = Schedule(
            effectiveDate=date(2025, 2, 28),
            terminationDate=date(2025, 6, 3),
            frequency='1M',
            businessDayConvention=Following(),
            endOfMonth=True,
            stubPeriod=ShortBack(),
            calendar=RussiaCalendar(),
            paymentLag=0
        )
        schedule = sampleSchedule.getSchedule()

        with self.subTest("start dates"):
            self.assertListEqual(
                [
                    date(2025, 2, 28),
                    date(2025, 3, 31),
                    date(2025, 4, 30),
                    date(2025, 5, 30)
                ],
                schedule.accrualStartDates
            )

        with self.subTest("end dates"):
            self.assertListEqual(
                [
                    date(2025, 3, 31),
                    date(2025, 4, 30),
                    date(2025, 5, 30),
                    date(2025, 6, 3)
                ],
                schedule.accrualEndDates
            )

    def testGetScheduleBack(self):
        self._effectiveDate = date(2025, 11, 4)
        terminationDate = date(2025, 12, 4)
        frequency = '1M'
        businessDayConvention = Following()
        endOfMonth = False
        stubPeriod = ShortBack()
        calendar = RussiaCalendar()

        _sampleSchedule = Schedule(
            effectiveDate=self._effectiveDate,
            terminationDate=terminationDate,
            frequency=frequency,
            businessDayConvention=businessDayConvention,
            endOfMonth=endOfMonth,
            stubPeriod=stubPeriod,
            calendar=calendar,
            paymentLag=1
        )
        schedule = _sampleSchedule.getSchedule()
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
