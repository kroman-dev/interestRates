from unittest import TestCase
from math import exp

from ir.dualNumbers.dualNumber import DualNumber


class DualNumberTest(TestCase):

    def setUp(self):
        self._dualNumber = DualNumber(
            realPart=3.,
            dualPart={'x': 2., 'y': -1.5}
        )

    def testNeg(self):
        negativeDualNumber = -self._dualNumber
        self.assertEqual(-3., negativeDualNumber._realPart)
        self.assertEqual({'x': -2., 'y': 1.5}, negativeDualNumber._dualPart)

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

    def testMul(self):
        with self.subTest("d_1 * d_2"):
            self.assertEqual(
                DualNumber(
                    realPart=6.,
                    dualPart={
                        'x': 2. * 3. + 4. * 2.,
                        'y': -1.5 * 2.,
                        'z': -1.5 * 3.
                    }
                ),
                DualNumber(realPart=2., dualPart={'x': 2., 'z': -1.5}) \
                * DualNumber(realPart=3., dualPart={'x': 4., 'y': -1.5})
            )

        with self.subTest("d_1 * const"):
            self.assertEqual(
                DualNumber(
                    realPart=8.,
                    dualPart={
                        'x': 8.,
                        'z': -6.
                    }
                ),
                DualNumber(realPart=2., dualPart={'x': 2., 'z': -1.5}) * 4
            )

        with self.subTest("const * d_1"):
            self.assertEqual(
                DualNumber(
                    realPart=8.,
                    dualPart={
                        'x': 8.,
                        'z': -6.
                    }
                ),
                4 * DualNumber(realPart=2., dualPart={'x': 2., 'z': -1.5})
            )

    def testConjugate(self):
        self.assertEqual(
            DualNumber(
                realPart=3.,
                dualPart={'x': -2., 'y': 1.5}
            ),
            self._dualNumber.conjugate()
        )

    def testTrueDiv(self):
        with self.subTest("d_1 / d_2"):
            self.assertEqual(
                DualNumber(
                    realPart=2. / 3.,
                    dualPart={
                        'x': (2. * 3. - 4. * 2.) / 9,
                        'y': 1.5 * 2. / 3. / 3.,
                        'z': -1.5 / 3.
                    }
                ),
                DualNumber(realPart=2., dualPart={'x': 2., 'z': -1.5}) \
                / DualNumber(realPart=3., dualPart={'x': 4., 'y': -1.5})
            )

        with self.subTest("d_1 * const"):
            self.assertEqual(
                DualNumber(
                    realPart=1.,
                    dualPart={
                        'x': 1.,
                        'z': -0.75
                    }
                ),
                DualNumber(realPart=2., dualPart={'x': 2., 'z': -1.5}) / 2
            )

        with self.subTest("const * d_1"):
            self.assertEqual(
                DualNumber(
                    realPart=2.,
                    dualPart={
                        'x': -2. * 4. / 4.,
                        'z': 1.5 * 4. / 4.
                    }
                ),
                4 / DualNumber(realPart=2., dualPart={'x': 2., 'z': -1.5})
            )

    def testExp(self):
        self.assertEqual(
            DualNumber(
                realPart=exp(2.),
                dualPart={'x': exp(2.)*2., 'z': -1.5 * exp(2.)}
            ),
            DualNumber(realPart=2., dualPart={'x': 2., 'z': -1.5}).__exp__()
        )

    def testLog(self):
        self.assertEqual(
            DualNumber(
                realPart=2.,
                dualPart={'x': 2. / exp(2.), 'z': -1.5 / exp(2.)}
            ),
            DualNumber(
                realPart=exp(2.),
                dualPart={'x': 2., 'z': -1.5}
            ).__log__()
        )

    def testPow(self):
        self.assertEqual(
            DualNumber(
                realPart=16,
                dualPart={'x': 96.}
            ),
            DualNumber(
                realPart=2,
                dualPart={'x': 3.}
            ).__pow__(4)
        )

    def testGeneral(self):

        def someFunc(x, y):
            return x**2 * y

        self.assertEqual(
            DualNumber(
                realPart=21.875,
                dualPart={'x': 17.5, 'y': 6.25}
            ),
            someFunc(
                x=DualNumber(
                    realPart=2.5,
                    dualPart={'x': 1}
                ),
                y=DualNumber(
                    realPart=3.5,
                    dualPart={'y': 1}
                )
            )
        )
