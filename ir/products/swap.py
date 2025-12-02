from ir.legs.genericLeg import GenericLeg


class Swap:

    def __init__(self, receiveLeg: GenericLeg, payLeg: GenericLeg):
        self._receiveLeg = receiveLeg
        self._payLeg = payLeg

    def npv(self) -> float:
        return self._receiveLeg.npv() - self._payLeg.npv()
