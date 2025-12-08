from datetime import date

from ir.curve.curveBootstrapping import CurveBootstrapping
from ir.curve.discountCurve import DiscountCurve
from ir.curve.interpolator.logLinearInterpolator import LogLinearInterpolator
from ir.dayCounter.act360 import Act360
from ir.products.interestRateSwap import InterestRateSwap
from ir.scheduler.businessDayConvention.following import Following
from ir.scheduler.calendar.unitedStatesNyseCalendar import \
    UnitedStatesNyseCalendar
from ir.scheduler.period.period import Period
from ir.scheduler.stubPeriod.shortBack import ShortBack


if __name__ == '__main__':
    dayCounter = Act360
    calendar = UnitedStatesNyseCalendar()
    businessDayConvention = Following()
    valueDate = date(2022, 1, 31)
    endOfMonth = False
    stubPeriod = ShortBack()
    fixFrequency = '1Y'
    floatFrequency = '3M'

    effectiveDate = calendar.advance(
        date=valueDate,
        period=Period('2D'),
        businessDayConvention=businessDayConvention,
        endOfMonth=endOfMonth
    )
    tenors = ['3M', '6M', '9M'] \
             + [f'{i}Y' for i in range(1, 11, 1)] \
             + ['12Y', '15Y', '20Y', '25Y', '30Y']

    # dates = [date(2022, 1, 31), effectiveDate]
    dates = [date(2022, 1, 31), date(2022, 1, 31)]
    # dates = [effectiveDate, effectiveDate]
    dates += [
        calendar.advance(
            date=effectiveDate,
            period=Period(tenor),
            businessDayConvention=businessDayConvention,
            endOfMonth=endOfMonth
        )
        for tenor in tenors
    ]

    values = [1. for _ in range(len(dates))]

    initialNodes = {
        _date: discountFactor
        for _date, discountFactor in zip(dates, values)
    }

    initialCurve = DiscountCurve(
        dates=dates,
        discountFactors=values,
        dayCounter=dayCounter
    )

    deposit = InterestRateSwap(
        curve=initialCurve,
        fixedRate=0.3 / 100,
        effectiveDate=dates[1],
        terminationDate=dates[2],
        fixFrequency='3M',
        floatFrequency='3M',
        endOfMonth=endOfMonth,
        businessDayConvention=businessDayConvention,
        dayCounter=dayCounter,
        stubPeriod=stubPeriod,
        calendar=calendar,
        notional=1.
    )

    fra1 = InterestRateSwap(
        curve=initialCurve,
        fixedRate=0.75 / 100,
        effectiveDate=dates[2],
        terminationDate=dates[3],
        fixFrequency='3M',
        floatFrequency='3M',
        endOfMonth=endOfMonth,
        businessDayConvention=businessDayConvention,
        dayCounter=dayCounter,
        stubPeriod=stubPeriod,
        calendar=calendar,
        notional=1.
    )

    fra2 = InterestRateSwap(
        curve=initialCurve,
        fixedRate=1.1 / 100,
        effectiveDate=dates[3],
        terminationDate=dates[4],
        fixFrequency='3M',
        floatFrequency='3M',
        endOfMonth=endOfMonth,
        businessDayConvention=businessDayConvention,
        dayCounter=dayCounter,
        stubPeriod=stubPeriod,
        calendar=calendar,
        notional=1.
    )

    createSwap = lambda fixedRate, terminationDate: InterestRateSwap(
        curve=initialCurve,
        fixedRate=fixedRate,
        effectiveDate=effectiveDate,
        terminationDate=terminationDate,
        fixFrequency=fixFrequency,
        floatFrequency=floatFrequency,
        endOfMonth=endOfMonth,
        businessDayConvention=businessDayConvention,
        dayCounter=dayCounter,
        stubPeriod=stubPeriod,
        calendar=calendar,
        notional=1.
    )

    swapQuotes = [
        quote / 100 for quote in [
            0.9000, 1.3300, 1.5300, 1.6300, 1.6900, 1.7300, 1.7700, 1.8000,
            1.8200, 1.8400, 1.8900, 1.9300, 1.9600, 1.9500, 1.9200
        ]
    ]

    swaps = [deposit, fra1, fra2] + [
        createSwap(fixRate, endDate)
        for fixRate, endDate in zip(swapQuotes, dates[5:])
    ]

    str(swaps[-1])

    curve, convergenceStatus = CurveBootstrapping(
        initialGuessNodes=initialNodes,
        swaps=swaps,
        dayCounter=dayCounter,
        curveInterpolator=LogLinearInterpolator
    ).solve()

    for swap in swaps:
        print(swap.npv(curve).realPart)

    df = curve.getDiscountFactor(date(2022, 4, 30)).realPart
    print(df)
    # print(1 / 0.25 * (1 / df - 1))
    # print(1 / 0.25 * (1 / (df + 1e-6) - 1))
