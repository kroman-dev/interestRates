from unittest import TestCase

import numpy as np

from ir.curve.interpolator.linearInterpolator import LinearInterpolator


class LinearInterpolatorTest(TestCase):

    def testInterpolate(self):
        testCases = [
            {
                "name": "left bound",
                "x1": 0.0,
                "x2": 10.0,
                "y1": 5.0,
                "y2": 15.0,
                "x": 0.0,
                "expected": 5.0
            },
            {
                "name": "right bound",
                "x1": 0.0,
                "x2": 10.0,
                "y1": 5.0,
                "y2": 15.0,
                "x": 10.0,
                "expected": 15.0
            },
            {
                "name": "midpoint",
                "x1": 0.0,
                "x2": 10.0,
                "y1": 5.0,
                "y2": 15.0,
                "x": 5.0,
                "expected": 10.0
            },
            {
                "name": "interpolateBetweenPoints",
                "x1": 1.0,
                "x2": 5.0,
                "y1": 2.0,
                "y2": 10.0,
                "x": 3.0,
                "expected": 6.0
            }
        ]

        for testCase in testCases:
            with self.subTest(testCase["name"]):
                interpolator = LinearInterpolator(
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
        """Test linear interpolation with vector input"""
        testCases = [
            {
                "name": "interpolateVectorInput",
                "x1": 0.0,
                "x2": 10.0,
                "y1": 0.0,
                "y2": 100.0,
                "x": np.array([0.0, 5.0, 10.0]),
                "expected": np.array([0.0, 50.0, 100.0])
            },
            {
                "name": "interpolateVectorInputNegative",
                "x1": -5.0,
                "x2": 5.0,
                "y1": 10.0,
                "y2": 20.0,
                "x": np.array([-5.0, 0.0, 5.0]),
                "expected": np.array([10.0, 15.0, 20.0])
            }
        ]

        for testCase in testCases:
            with self.subTest(testCase["name"]):
                interpolator = LinearInterpolator(
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

