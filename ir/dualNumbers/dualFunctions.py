import math

from ir.dualNumbers.dualNumber import DualNumber


def exp(x):
    if isinstance(x, DualNumber):
        return x.__exp__()
    return math.exp(x)


def log(x):
    if isinstance(x, DualNumber):
        return x.__log__()
    return math.log(x)
