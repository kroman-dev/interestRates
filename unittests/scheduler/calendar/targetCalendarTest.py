import datetime

from unittest import TestCase

from ir.scheduler.calendar.targetCalendar import \
    TargetCalendar
from ir.scheduler.period.period import Period
from ir.scheduler.businessDayConvention.following import Following


class TargetCalendarTest(TestCase):

    def setUp(self):
        self._sampleCalendar = TargetCalendar()

    def testIsBusinessDay(self):
        with self.subTest("False weekend"):
            self.assertEqual(
                False,
                self._sampleCalendar.isBusinessDay(
                    datetime.date(2025, 11, 29)
                )
            )

        with self.subTest("True 1"):
            self.assertEqual(
                True,
                self._sampleCalendar.isBusinessDay(
                    datetime.date(2025, 11, 4)
                )
            )

        with self.subTest("Thanksgiving"):
            self.assertEqual(
                True,
                self._sampleCalendar.isBusinessDay(
                    datetime.date(2025, 11, 27)
                )
            )

        with self.subTest("date(2045, 11, 27)"):
            self.assertEqual(
                True,
                self._sampleCalendar.isBusinessDay(
                    datetime.date(2045, 11, 27)
                )
            )

    def testAdvance(self):
        with self.subTest("0D"):
            self.assertEqual(
                datetime.date(2025, 11, 17),
                self._sampleCalendar.advance(
                    date=datetime.date(2025, 11, 15),
                    period=Period('0D'),
                    businessDayConvention=Following,
                    endOfMonth=False
                )
            )

        with self.subTest("0D"):
            self.assertEqual(
                datetime.date(2025, 11, 14),
                self._sampleCalendar.advance(
                    date=datetime.date(2025, 11, 14),
                    period=Period('0D'),
                    businessDayConvention=Following,
                    endOfMonth=False
                )
            )

        with self.subTest("endOfMonth=True 2025.11.30"):
            self.assertEqual(
                datetime.date(2025, 12, 30),
                self._sampleCalendar.advance(
                    date=datetime.date(2025, 11, 30),
                    period=Period('1M'),
                    businessDayConvention=Following,
                    endOfMonth=True
                )
            )

        with self.subTest("endOfMonth=True 2025.10.30"):
            self.assertEqual(
                datetime.date(2025, 12, 1),
                self._sampleCalendar.advance(
                    date=datetime.date(2025, 10, 30),
                    period=Period('1M'),
                    businessDayConvention=Following,
                    endOfMonth=True
                )
            )

        with self.subTest("endOfMonth=True 2025.10.31"):
            self.assertEqual(
                datetime.date(2025, 11, 28),
                self._sampleCalendar.advance(
                    date=datetime.date(2025, 10, 31),
                    period=Period('1M'),
                    businessDayConvention=Following,
                    endOfMonth=True
                )
            )

        with self.subTest("endOfMonth=False 2025.10.31"):
            self.assertEqual(
                datetime.date(2025, 12, 1),
                self._sampleCalendar.advance(
                    date=datetime.date(2025, 10, 31),
                    period=Period('1M'),
                    businessDayConvention=Following,
                    endOfMonth=False
                )
            )

        with self.subTest("endOfMonth=False"):
            self.assertEqual(
                datetime.date(2025, 12, 30),
                self._sampleCalendar.advance(
                    date=datetime.date(2025, 11, 30),
                    period=Period('1M'),
                    businessDayConvention=Following,
                    endOfMonth=False
                )
            )

        with self.subTest("Following"):
            self.assertEqual(
                datetime.date(2025, 11, 24),
                self._sampleCalendar.advance(
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
                self._sampleCalendar.retreat(
                    date=datetime.date(2025, 11, 14),
                    period=Period('0D'),
                    businessDayConvention=Following,
                    endOfMonth=False
                )
            )

        with self.subTest("endOfMonth=True"):
            self.assertEqual(
                datetime.date(2025, 10, 14),
                self._sampleCalendar.retreat(
                    date=datetime.date(2025, 11, 14),
                    period=Period('1M'),
                    businessDayConvention=Following,
                    endOfMonth=True
                )
            )

        with self.subTest("endOfMonth=False"):
            self.assertEqual(
                datetime.date(2025, 10, 14),
                self._sampleCalendar.retreat(
                    date=datetime.date(2025, 11, 14),
                    period=Period('1M'),
                    businessDayConvention=Following,
                    endOfMonth=False
                )
            )

        with self.subTest("endOfMonth=False 2"):
            self.assertEqual(
                datetime.date(2025, 10, 20),
                self._sampleCalendar.retreat(
                    date=datetime.date(2025, 11, 18),
                    period=Period('1M'),
                    businessDayConvention=Following,
                    endOfMonth=False
                )
            )

    def testIsLastMonthBusinessDay(self):
        with self.subTest("28.11.2025"):
            self.assertTrue(
                self._sampleCalendar.isLastMonthBusinessDay(
                    datetime.date(2025, 11, 28)
                )
            )

        with self.subTest("29.11.2025"):
            self.assertFalse(
                self._sampleCalendar.isLastMonthBusinessDay(
                    datetime.date(2025, 11, 29)
                )
            )

        with self.subTest("15.11.2025"):
            self.assertFalse(
                self._sampleCalendar.isLastMonthBusinessDay(
                    datetime.date(2025, 11, 15)
                )
            )

    def testGetLastMonthBusinessDay(self):
        with self.subTest("28.11.2025"):
            self.assertEqual(
                datetime.date(2025, 11, 28),
                self._sampleCalendar.getLastMonthBusinessDay(
                    datetime.date(2025, 11, 15)
                )
            )
