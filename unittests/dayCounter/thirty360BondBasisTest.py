import datetime
from unittest import TestCase

from ir.dayCounter.thirty360BondBasis import Thirty360BondBasis


class Thirty360BondBasisTest(TestCase):

    def testYearFraction(self):
        """Test year fraction calculation with various date combinations"""
        testCases = [
            {
                "name": "samy days",
                "startDate": datetime.date(2024, 1, 15),
                "endDate": datetime.date(2024, 2, 15),
                "expected": 30.0 / 360.0
            },
            {
                "name": "sameMonth",
                "startDate": datetime.date(2024, 3, 10),
                "endDate": datetime.date(2024, 3, 25),
                "expected": 15.0 / 360.0
            },
            {
                "name": "startDate31st",
                "startDate": datetime.date(2024, 1, 31),
                "endDate": datetime.date(2024, 2, 28),
                "expected": 28.0 / 360.0
            },
            {
                "name": "endDate31stWhenStartIs30",
                "startDate": datetime.date(2025, 9, 30),
                "endDate": datetime.date(2025, 10, 31),
                "expected": 30.0 / 360.0
            },
            {
                "name": "endDate31stWhenStartIsNot30",
                "startDate": datetime.date(2024, 2, 15),
                "endDate": datetime.date(2024, 3, 31),
                "expected": 46.0 / 360.0
            },
            {
                "name": "bothDates31st",
                "startDate": datetime.date(2024, 7, 31),
                "endDate": datetime.date(2024, 8, 31),
                "expected": 30.0 / 360.0
            },
            {
                "name": "fullYear",
                "startDate": datetime.date(2024, 1, 1),
                "endDate": datetime.date(2025, 1, 1),
                "expected": 1.0
            },
            {
                "name": "multipleYears",
                "startDate": datetime.date(2020, 1, 15),
                "endDate": datetime.date(2023, 6, 20),
                "expected": (360 * 3 + 30 * 5 + (20 - 15)) / 360.0
            },
            {
                "name": "leapYear",
                "startDate": datetime.date(2024, 2, 28),
                "endDate": datetime.date(2024, 3, 1),
                "expected": 3.0 / 360.0
            },
            {
                "name": "start31End29",
                "startDate": datetime.date(2024, 1, 31),
                "endDate": datetime.date(2024, 2, 29),
                "expected": 29.0 / 360.0
            },
            {
                "name": "sameDate",
                "startDate": datetime.date(2024, 6, 15),
                "endDate": datetime.date(2024, 6, 15),
                "expected": 0.0
            },
            {
                "name": "start31SameMonth",
                "startDate": datetime.date(2024, 1, 31),
                "endDate": datetime.date(2024, 1, 31),
                "expected": 0.0
            }
        ]

        for testCase in testCases:
            with self.subTest(testCase["name"]):
                self.assertAlmostEqual(
                    Thirty360BondBasis.yearFraction(
                        testCase["startDate"],
                        testCase["endDate"]
                    ),
                    testCase["expected"],
                    places=10,
                    msg=f"Failed for {testCase['name']}"
                )

