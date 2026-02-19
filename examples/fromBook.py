import pandas as pd
from bookirds.curves import *
from bookirds.dual import Dual


if __name__ == '__main__':
    nodes = {
        datetime(2022, 1, 1): Dual(1, {"v0": 1}),
        datetime(2023, 1, 1): Dual(1, {"v1": 1}),
        datetime(2024, 1, 1): Dual(1, {"v2": 1}),
        datetime(2027, 1, 1): Dual(1, {"v3": 1}),
        datetime(2032, 1, 1): Dual(1, {"v4": 1})
    }
    notional = 100e6
    swaps = {
        Swap(datetime(2022, 1, 1), 12 * 1, 12, 12, notional=notional): 1.210,
        Swap(datetime(2022, 1, 1), 12 * 2, 12, 12, notional=notional): 1.635,
        Swap(datetime(2022, 1, 1), 12 * 5, 12, 12, notional=notional): 1.885,
        Swap(datetime(2022, 1, 1), 12 * 10, 12, 12, notional=notional): 1.930
    }
    sampleSolvedCurve = SolvedCurve(
        nodes=nodes,
        swaps=list(swaps.keys()),
        obj_rates=list(swaps.values()),
        interpolation="log_linear",
        algorithm="levenberg_marquardt"
    )
    print(sampleSolvedCurve.iterate())

    for swap in swaps.keys():
        print(swap.rate(sampleSolvedCurve).real)

    risk = {}
    for swap in swaps.keys():
        risk.update({swap.end: swap.risk(sampleSolvedCurve)[:, 0]})

    df = pd.DataFrame(risk, index=["1y", "2y", "5y", "10y"])
    df.style.format("{:.3f}")

    print(df)
    """
             2023-01-01    2024-01-01    2027-01-01    2032-01-01
    1y    98.804467 -4.755842e-09  6.627692e-09 -5.634680e-08
    2y     0.000000  1.956063e+02  3.257251e-08 -2.125996e-07
    5y     0.000000  0.000000e+00  4.746887e+02 -6.777909e-07
    10y    0.000000  0.000000e+00  0.000000e+00  9.043337e+02
    """
