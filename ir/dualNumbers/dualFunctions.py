import numpy as np

from ir.dualNumbers.dualNumber import DualNumber


def exp(x):
    if isinstance(x, DualNumber):
        return x.__exp__()
    return np.exp(x)

def log(x):
    if isinstance(x, DualNumber):
        return x.__log__()
    return np.log(x)
