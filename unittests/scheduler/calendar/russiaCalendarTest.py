import datetime

from unittest import TestCase

from ir.scheduler.calendar.russiaCalendar import RussiaCalendar
from ir.scheduler.period.period import Period
from ir.scheduler.businessDayConvention.following import Following


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

    def testAdvance(self):
        with self.subTest("endOfMonth=True"):
            self.assertEqual(
                datetime.date(2025, 12, 31),
                self._sampleRussiaCalendar.advance(
                    date=datetime.date(2025, 11, 30),
                    period=Period('1M'),
                    businessDayConvention=Following,
                    endOfMonth=True
                )
            )

        with self.subTest("endOfMonth=False"):
            self.assertEqual(
                datetime.date(2025, 12, 30),
                self._sampleRussiaCalendar.advance(
                    date=datetime.date(2025, 11, 30),
                    period=Period('1M'),
                    businessDayConvention=Following,
                    endOfMonth=False
                )
            )

        with self.subTest("Following"):
            self.assertEqual(
                datetime.date(2025, 11, 24),
                self._sampleRussiaCalendar.advance(
                    date=datetime.date(2025, 10, 23),
                    period=Period('1M'),
                    businessDayConvention=Following,
                    endOfMonth=False
                )
            )
