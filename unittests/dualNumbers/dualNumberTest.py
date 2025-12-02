from unittest import TestCase

from ir.dualNumbers.dualNumber import DualNumber


class DualNumberTest(TestCase):

    def setUp(self):

        self._dualNumber = DualNumber(
            realPart=3.0,
            dualPart={'x': 2.0, 'y': -1.5}
        )

    def testNeg(self):
        neg = -self._dualNumber
        self.assertEqual(-3.0, neg._realPart)
        self.assertEqual({'x': -2.0, 'y': 1.5}, neg._dualPart)

