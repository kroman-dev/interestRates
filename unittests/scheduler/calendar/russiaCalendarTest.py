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
        with self.subTest("0D"):
            self.assertEqual(
                datetime.date(2025, 11, 17),
                self._sampleRussiaCalendar.advance(
                    date=datetime.date(2025, 11, 15),
                    period=Period('0D'),
                    businessDayConvention=Following,
                    endOfMonth=False
                )
            )

        with self.subTest("0D"):
            self.assertEqual(
                datetime.date(2025, 11, 14),
                self._sampleRussiaCalendar.advance(
                    date=datetime.date(2025, 11, 14),
                    period=Period('0D'),
                    businessDayConvention=Following,
                    endOfMonth=False
                )
            )

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

    def testRetreat(self):
        with self.subTest("0D"):
            self.assertEqual(
                datetime.date(2025, 11, 14),
                self._sampleRussiaCalendar.retreat(
                    date=datetime.date(2025, 11, 14),
                    period=Period('0D'),
                    businessDayConvention=Following,
                    endOfMonth=False
                )
            )

        with self.subTest("endOfMonth=True"):
            self.assertEqual(
                datetime.date(2025, 10, 31),
                self._sampleRussiaCalendar.retreat(
                    date=datetime.date(2025, 11, 14),
                    period=Period('1M'),
                    businessDayConvention=Following,
                    endOfMonth=True
                )
            )

        with self.subTest("endOfMonth=False"):
            self.assertEqual(
                datetime.date(2025, 10, 14),
                self._sampleRussiaCalendar.retreat(
                    date=datetime.date(2025, 11, 14),
                    period=Period('1M'),
                    businessDayConvention=Following,
                    endOfMonth=False
                )
            )

        with self.subTest("endOfMonth=False 2"):
            self.assertEqual(
                datetime.date(2025, 10, 20),
                self._sampleRussiaCalendar.retreat(
                    date=datetime.date(2025, 11, 18),
                    period=Period('1M'),
                    businessDayConvention=Following,
                    endOfMonth=False
                )
            )

    def testIsLastMonthBusinessDay(self):
        with self.subTest("28.11.2025"):
            self.assertTrue(
                self._sampleRussiaCalendar.isLastMonthBusinessDay(
                    datetime.date(2025, 11, 28)
                )
            )

        with self.subTest("29.11.2025"):
            self.assertFalse(
                self._sampleRussiaCalendar.isLastMonthBusinessDay(
                    datetime.date(2025, 11, 29)
                )
            )

        with self.subTest("15.11.2025"):
            self.assertFalse(
                self._sampleRussiaCalendar.isLastMonthBusinessDay(
                    datetime.date(2025, 11, 15)
                )
            )
