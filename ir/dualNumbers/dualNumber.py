from typing import Dict, Optional, Any


class DualNumber:

    def __init__(
            self,
            realPart: float,
            dualPart: Optional[Dict[str, float]] = None
    ):
        """
        A dual number is z = a + b \epsilon,
         where a, b are real and \epsilon such that \epsilon ** 2 = 0 and
         \epsilon != 0

         arithmetic:
            1) negation: -z = -a - b \epsilon
            2) equality: z_1=z_2 => a_1=a_2 and b_1=b_2
            3) addition: z_1 + z_2 = (a_1 + a_2) + (b_1 + b_2) \epsilon
            4) subtraction: z_1 - z_2 = a_1 - a_2 + (b_1 - b_2) \epsilon
            5) multiplication: z_1 * z_2 =
                            = a_1 * a_2 + (b_1 * a_2 + b_2 * a_1) \epsilon
            6) conjugate: \overline{z_1} = a_1 - b_1 \epsilon
            7) division: z_1 / z_2 = \cfrac{
                    a_1 * a_2 + (b_1 * a_2 - b_2 * a_1)\epsilon
                }{a_2 **2 }
        """
        self._realPart = realPart
        self._dualPart = {} if dualPart is None else dualPart.copy()

    @property
    def realPart(self) -> float:
        return self._realPart

    @property
    def dualPart(self) -> Optional[Dict[str, float]]:
        return self._dualPart

    def __neg__(self) -> 'DualNumber':
            return DualNumber(
                realPart=-self.realPart,
                dualPart={key: -value for key, value in self.dualPart.items()}
            )

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, DualNumber):
            return False

        return (self.realPart == other.realPart) \
            and (self.dualPart == other.dualPart)

    def __add__(self, other: Any) -> 'DualNumber':

        if isinstance(other, DualNumber):
            newDualPart = self.dualPart.copy()
            for otherKey, otherValue in other.dualPart.items():
                newDualPart[otherKey] = other.dualPart[otherKey] \
                    if newDualPart.get(otherKey) is None \
                    else newDualPart[otherKey] + other.dualPart[otherKey]

            return DualNumber(
                realPart=self.realPart + other.realPart,
                dualPart=newDualPart
            )

        return DualNumber(
            realPart=self.realPart + other,
            dualPart=self.dualPart
        )

    def __radd__(self, other) -> 'DualNumber':
        return self.__add__(other)

    def __sub__(self, other) -> 'DualNumber':
        return self.__add__(-other)

    def __rsub__(self, other) -> 'DualNumber':
        return -(self - other)

    def __mul__(self, other: Any) -> 'DualNumber':
        if isinstance(other, DualNumber):
            newDualPart = {
                key: value * other.realPart
                for key, value in self.dualPart.items()
            }
            for otherKey, otherValue in other.dualPart.items():
                otherDualTerm = self.realPart * other.dualPart[otherKey]
                newDualPart[otherKey] = otherDualTerm \
                    if newDualPart.get(otherKey) is None \
                    else newDualPart.get(otherKey) + otherDualTerm

            return DualNumber(
                realPart=self.realPart * other.realPart,
                dualPart=newDualPart
            )

        return DualNumber(
            realPart=self.realPart * other,
            dualPart={key: value*other for key, value in self.dualPart.items()}
        )

    def __rmul__(self, other) -> 'DualNumber':
        return self.__mul__(other)

    def conjugate(self) -> 'DualNumber':
        return DualNumber(
            realPart=self.realPart,
            dualPart={key: -value for key, value in self.dualPart.items()}
        )
