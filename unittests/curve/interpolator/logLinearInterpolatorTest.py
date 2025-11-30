from unittest import TestCase

import numpy as np

from ir.curve.interpolator.logLinearInterpolator import LogLinearInterpolator


class LogLinearInterpolatorTest(TestCase):

    def testInterpolate(self):

        testCases = [
            {
                "name": "left bound",
                "x1": 0.0,
                "x2": 10.0,
                "y1": 1.0,
                "y2": 100.0,
                "x": 0.0,
                "expected": 1.0
            },
            {
                "name": "right bound",
                "x1": 0.0,
                "x2": 10.0,
                "y1": 1.0,
                "y2": 100.0,
                "x": 10.0,
                "expected": 100.0
            },
            {
                "name": "mid",
                "x1": 0.0,
                "x2": 2.0,
                "y1": 1.0,
                "y2": 100.0,
                "x": 1.0,
                "expected": 10.0
            },
            {
                "name": "interpolateBetweenPoints",
                "x1": 1.0,
                "x2": 3.0,
                "y1": 10.0,
                "y2": 1000.0,
                "x": 2.0,
                "expected": 100.0
            }
        ]

        for testCase in testCases:
            with self.subTest(testCase["name"]):
                interpolator = LogLinearInterpolator(
                    x1=testCase["x1"],
                    x2=testCase["x2"],
                    y1=testCase["y1"],
                    y2=testCase["y2"]
                )
                result = interpolator(testCase["x"])
                self.assertAlmostEqual(
                    result,
                    testCase["expected"],
                    places=10,
                    msg=f"Failed for {testCase['name']}"
                )

    def testInterpolateWithVector(self):

        testCases = [
            {
                "name": "interpolateVectorInput",
                "x1": 0.0,
                "x2": 2.0,
                "y1": 1.0,
                "y2": 100.0,
                "x": np.array([0.0, 1.0, 2.0]),
                "expected": np.array([1.0, 10.0, 100.0])
            },
            {
                "name": "interpolateVectorInputExponential",
                "x1": 0.0,
                "x2": 1.0,
                "y1": 2.0,
                "y2": 8.0,
                "x": np.array([0.0, 0.5, 1.0]),
                "expected": np.array([2.0, 4.0, 8.0])
            }
        ]

        for testCase in testCases:
            with self.subTest(testCase["name"]):
                interpolator = LogLinearInterpolator(
                    x1=testCase["x1"],
                    x2=testCase["x2"],
                    y1=testCase["y1"],
                    y2=testCase["y2"]
                )
                result = interpolator(testCase["x"])
                np.testing.assert_array_almost_equal(
                    result,
                    testCase["expected"],
                    decimal=10,
                    err_msg=f"Failed for {testCase['name']}"
                )

