import datetime

from unittest import TestCase

from ir.scheduler.calendar.russiaCalendar import RussiaCalendar


class RussiaCalendarTest(TestCase):

    def setUp(self):
        self._sampleRussiaCalendar = RussiaCalendar()

    def testIsBusinessDay(self):
        with self.subTest("False weekend"):
            self.assertEqual(
                False,
                self._sampleRussiaCalendar.isBusinessDay(
                    datetime.date(2025, 11, 29)
                )
            )

        with self.subTest("False addHoliday"):
            self.assertEqual(
                False,
                self._sampleRussiaCalendar.isBusinessDay(
                    datetime.date(2025, 11, 4)
                )
            )

        with self.subTest("True"):
            self.assertEqual(
                True,
                self._sampleRussiaCalendar.isBusinessDay(
                    datetime.date(2025, 11, 27)
                )
            )
