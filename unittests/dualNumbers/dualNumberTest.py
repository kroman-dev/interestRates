from unittest import TestCase

from ir.dualNumbers.dualNumber import DualNumber


class DualNumberTest(TestCase):

    def setUp(self):
        self._dualNumber = DualNumber(
            realPart=3.,
            dualPart={'x': 2., 'y': -1.5}
        )

    def testNeg(self):
        neg = -self._dualNumber
        self.assertEqual(-3., neg._realPart)
        self.assertEqual({'x': -2., 'y': 1.5}, neg._dualPart)

    def testEq(self):
        with self.subTest("True case"):
            self.assertTrue(
                DualNumber(
                    realPart=3.,
                    dualPart={'x': 2., 'y': -1.5}
                ) == self._dualNumber
            )
        with self.subTest("False case"):
            self.assertFalse(
                DualNumber(
                    realPart=2.,
                    dualPart={'x': 2., 'y': -1.5}
                ) == self._dualNumber
            )

    def testAdd(self):
        with self.subTest("d_1 + d_1"):
            self.assertEqual(
                DualNumber(realPart=6., dualPart={'x': 4., 'y': -3.}),
                self._dualNumber + self._dualNumber
            )

        with self.subTest("d_1 + 3"):
            self.assertEqual(
                DualNumber(realPart=6., dualPart={'x': 2., 'y': -1.5}),
                self._dualNumber + 3.
            )

        with self.subTest("3 + d_1"):
            self.assertEqual(
                DualNumber(realPart=6., dualPart={'x': 2., 'y': -1.5}),
                3. + self._dualNumber
            )

        with self.subTest("d_1 + d_2"):
            self.assertEqual(
                DualNumber(
                    realPart=5.,
                    dualPart={'x': 4., 'y': -1.5, 'z': -1.5}
                ),
                DualNumber(realPart=3., dualPart={'x': 2., 'y': -1.5}) \
                + DualNumber(realPart=2., dualPart={'x': 2., 'z': -1.5})
            )

    def testSub(self):
        with self.subTest("d_1 - d_1"):
            self.assertEqual(
                DualNumber(realPart=0., dualPart={'x': 0., 'y': 0.}),
                self._dualNumber - self._dualNumber
            )

        with self.subTest("d_1 - 3"):
            self.assertEqual(
                DualNumber(realPart=0., dualPart={'x': 2., 'y': -1.5}),
                self._dualNumber - 3.
            )

        with self.subTest("d_1 - d_2"):
            self.assertEqual(
                DualNumber(
                    realPart=1.,
                    dualPart={'x': 0., 'y': -1.5, 'z': 1.5}
                ),
                DualNumber(realPart=3., dualPart={'x': 2., 'y': -1.5}) \
                - DualNumber(realPart=2., dualPart={'x': 2., 'z': -1.5})
            )

    def testRSub(self):
        with self.subTest("d_1 - d_1"):
            self.assertEqual(
                DualNumber(realPart=0., dualPart={'x': 0., 'y': 0.}),
                self._dualNumber - self._dualNumber
            )

        with self.subTest("-d_1 - d_2"):
            self.assertEqual(
                DualNumber(
                    realPart=-5.,
                    dualPart={'x': -4., 'y': 1.5, 'z': 1.5}
                ),
                -DualNumber(realPart=3., dualPart={'x': 2., 'y': -1.5}) \
                -DualNumber(realPart=2., dualPart={'x': 2., 'z': -1.5})
            )

        with self.subTest("3 - d_1"):
            self.assertEqual(
                DualNumber(realPart=0., dualPart={'x': -2., 'y': 1.5}),
                3. - self._dualNumber
            )
