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
            calendar=NoCalendar(),
            notional=1e6
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

    # jacobian = sampleBootstrappingSolver._getJacobianOfCurveDiscountFactors()
    # curve.setJacobian(jacobian)

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
        notional=1e6
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
        notional=1e6
    )
    # print(curve.getJacobian())
    # print()

    """
    [[ 0.         -0.9894525   0.01613477  0.01761811  0.01638691]
     [ 0.          0.         -1.95027432  0.07081905  0.06587004]
     [ 0.          0.          0.         -4.62965384  0.33777038]
     [ 0.          0.          0.          0.         -8.63510294]]
    """

    # for swap in swaps:
    #     print(swap.npv(curve))

    # print(testSwap.npv(curve) / 1000000)


    for value in testSwap.getDeltas(curve).squeeze():
        print(f"{float(value): .10}")

    """ 
        -0.04632009117
        -0.18619166
        -480.9582688
         916.9526568
    """

    print()


    for swap in swaps:
        print(swap.getDeltas(curve).squeeze())
        print()

