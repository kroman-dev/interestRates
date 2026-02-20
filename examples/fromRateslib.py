import pandas as pd
from rateslib import *


def curve_factory(interpolation, t):
    return Curve(
        nodes={
            dt(2022, 1, 1): 1.0,
            dt(2023, 1, 1): 1.0,
            dt(2024, 1, 1): 1.0,
            dt(2027, 1, 1): 1.0,
            dt(2032, 1, 1): 1.0,
        },
        convention="act360",
        calendar="all",
        interpolation=interpolation,
        t=t,
    )


if __name__ == '__main__':
    log_linear_curve = curve_factory(
        "log_linear",
        NoInput(0)
    )
    args = dict(
        calendar="all",
        frequency="a",
        convention="act360",
        payment_lag=0,
        curves=log_linear_curve,
        notional=100e6
    )
    instruments = [
        IRS(dt(2022, 1, 1), "1y", **args),
        IRS(dt(2022, 1, 1), "2y", **args),
        IRS(dt(2022, 1, 1), "5y", **args),
        IRS(dt(2022, 1, 1), "10y", **args)
    ]

    solver = Solver(
        curves=[log_linear_curve],
        instruments=instruments,
        s=[1.21, 1.635, 1.885, 1.93],
        instrument_labels=["1y", "2y", "5y", "10y"]
    )

    df = pd.DataFrame(
        index=[_ for _ in log_linear_curve.nodes.keys],
        data={
            "log-linear": [float(_) for _ in log_linear_curve.nodes.values]
        }
    )

    print(df)
    """
                log-linear
    2022-01-01    1.000000
    2023-01-01    0.987881
    2024-01-01    0.967584
    2027-01-01    0.909344
    2032-01-01    0.823282
    """
    # jacobian
    print(solver.grad_s_vT)

    exit()
    """
    [[-9.89462410e-03  1.61349307e-04  1.76182864e-04  1.63870778e-04]
     [-4.43104111e-20 -1.95029377e-02  7.08195898e-04  6.58705448e-04]
     [-2.90108784e-20  3.94717353e-19 -4.62974656e-02  3.37774209e-03]
     [-1.01643954e-20  3.25260652e-19 -5.63785130e-18 -8.63536457e-02]]
    """
    print()

    for index, instrument in enumerate(instruments):
        # print(instrument.npv(curves=[log_linear_curve]).real)
        print(f"npv: {instrument.npv(curves=[log_linear_curve]).dual / 1000000}")
        # print(instrument.npv(solver=solver).dual)

    forwardIrs = IRS(dt(2027, 1, 1), "5y", **args)

    print(forwardIrs.npv(curves=[log_linear_curve]).dual / 1000000)

    """
    [ 1.         -1.01226806  0.          0.          0.        ]
    [ 1.         -0.01657708 -1.01657708  0.          0.        ]
    [ 1.         -0.01911181 -0.037721   -1.03879498  0.        ]
    [ 1.         -0.01956806 -0.0386215  -0.07735915 -1.06033331]
    [ 0.          0.          0.          0.96139106 -1.06188966]
    the last row is my case
    """

    print(forwardIrs.delta(solver=solver).to_numpy().squeeze())

    # [-4.63205423e-02 -1.86193011e-01 -4.80967590e+02  9.16980438e+02]

    # print(
    #     IRS(
    #         dt(2027, 1, 1), "5y", **args
    #     ).npv(solver=solver).dual / 1000000
    # )

    # result = np.zeros((4,4))
    # for index, instrument in enumerate(instruments):
    #     result[index, :] = instrument.delta(solver=solver).to_numpy().squeeze()
    # print(result)
