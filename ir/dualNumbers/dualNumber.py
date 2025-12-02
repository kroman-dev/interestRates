from typing import Dict, Optional


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
            2) equality
        """
        self._realPart = realPart
        self._dualPart = {} if dualPart is None else dualPart.copy()

    def __neg__(self) -> 'DualNumber':
        return DualNumber(
            realPart=-self._realPart,
            dualPart={key: -value for key, value in self._dualPart.items()}
        )
