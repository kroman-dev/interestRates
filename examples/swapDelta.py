from datetime import date

from ir import *
from ir.scheduler.businessDayConvention.noConvention import NoConvention
from ir.scheduler.calendar.noCalendar import NoCalendar

if __name__ == '__main__':
    startDate = date(2022, 1, 1)
    swapsData = {
        '1Y': 1.210 / 100,
        '2Y': 1.635 / 100,
        '5Y': 1.885 / 100,
        '10Y': 1.930 / 100
    }
    frequency = '1Y'
    dayCounter = Act360()
    dates = [startDate] + [startDate + Period(tenor) for tenor in swapsData]

    swaps = [
        InterestRateSwap(
            fixedRate=fixedRate,
            effectiveDate=startDate,
            terminationDate=startDate + Period(tenor),
            fixFrequency=frequency,
            floatFrequency=frequency,
            endOfMonth=False,
            businessDayConvention=NoConvention(),
            dayCounter=dayCounter,
            stubPeriod=ShortBack(),
            calendar=NoCalendar()
        )
        for tenor, fixedRate in swapsData.items()
    ]

    sampleBootstrappingSolver = BootstrappingSolver(
        initialGuessNodes={_date: 1 for _date in dates},
        instruments=swaps,
        instrumentsQuotes=list(swapsData.values()),
        dayCounter=dayCounter
    )
    curve, status = sampleBootstrappingSolver.solve()

    jacobian = sampleBootstrappingSolver._getJacobianOfCurveDiscountFactors()
    curve.setJacobian(jacobian)

    parRate = InterestRateSwap(
        fixedRate=0.,
        effectiveDate=startDate + Period('5Y'),
        terminationDate=startDate + Period('10Y'),
        fixFrequency=frequency,
        floatFrequency=frequency,
        endOfMonth=False,
        businessDayConvention=NoConvention(),
        dayCounter=dayCounter,
        stubPeriod=ShortBack(),
        calendar=NoCalendar(),
        notional=100e6
    ).getParRate(curve)

    testSwap = InterestRateSwap(
        fixedRate=parRate.realPart,
        effectiveDate=startDate + Period('5Y'),
        terminationDate=startDate + Period('10Y'),
        fixFrequency=frequency,
        floatFrequency=frequency,
        endOfMonth=False,
        businessDayConvention=NoConvention(),
        dayCounter=dayCounter,
        stubPeriod=ShortBack(),
        calendar=NoCalendar(),
        notional=1
    )
    print(curve.getJacobian())
    print()

    """
    [[-0.98847235  0.01611879  0.01760066  0.01637068]
     [ 0.         -1.94835058  0.07076585  0.06582056]
     [ 0.          0.         -4.62048762  0.33739163]
     [ 0.          0.          0.         -8.60924359]]
    """

    for swap in swaps:
        print(swap.npv(curve))

    print()

    print(testSwap.npv(curve) / 1000000)

    #     f = -0.000000
    # df / dv2 = -0.0000
    # df / dv3 = 96.1391
    # df / dv4 = -106.1890

    for value in testSwap.getDeltas(curve).squeeze():
        print(f"{float(value): .10}")

    # [[-4.63200912e-02]
    #  [-1.86191660e-01]
    #  [-4.80958269e+02]
    #  [9.16952657e+02]]

import holidays_ru
