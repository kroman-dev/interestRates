import os
import datetime
import pandas as pd

from ir import *


if __name__ == '__main__':
    mainDir = os.path.dirname(os.path.abspath(""))
    eoniaDataframe = pd.read_csv(
        os.path.abspath(os.path.join(mainDir, "data/eonia11122012.csv")),
        sep=';'
    )
    eoniaDataframe['StartDate'] = eoniaDataframe['Start Date'].apply(
        lambda x: datetime.datetime.strptime(x, '%a %d %b %Y').date()
    )
    eoniaDataframe['EndDate'] = eoniaDataframe['End Date'].apply(
        lambda x: datetime.datetime.strptime(x, '%a %d %b %Y').date()
    )
    eoniaDataframe['Rate'] = eoniaDataframe['Rate, %'] / 100

    todayDate = eoniaDataframe.StartDate[0]
    spotDate = todayDate + Period('2D')

    stubPeriod = ShortBack()
    calendar = TargetCalendar()
    businessDayConvention = Following()
    endOfMonth = False
    dayCounter = Act360()
    dates = [todayDate] + eoniaDataframe["EndDate"].tolist()

    initialNodes = {_date: 1 for _date in dates}
    initialCurve = DiscountCurve(
        dates=list(initialNodes.keys()),
        discountFactors=list(initialNodes.values()),
        dayCounter=Act360()
    )

    # deposits
    instruments = [
        Deposit(
            curve=initialCurve,
            fixedRate=rate,
            effectiveDate=effectiveDate,
            tenor='1D',
            endOfMonth=endOfMonth,
            businessDayConvention=businessDayConvention,
            dayCounter=dayCounter,
            stubPeriod=stubPeriod,
            calendar=calendar,
            notional=1.
        )
        for rate, effectiveDate, terminationDate in zip(
            eoniaDataframe.Rate[:3].tolist(),
            dates[:3],
            dates[1:4]
        )
    ]

    # from 1W to 1M OIS
    instruments += [
        InterestRateSwap(
            discountCurve=initialCurve,
            fixedRate=rate,
            effectiveDate=spotDate,
            terminationDate=terminationDate,
            fixFrequency='1Y',
            floatFrequency='1Y',
            endOfMonth=endOfMonth,
            businessDayConvention=businessDayConvention,
            dayCounter=dayCounter,
            stubPeriod=stubPeriod,
            calendar=calendar,
            notional=1.
        )
        for rate, terminationDate in zip(
            eoniaDataframe.Rate[3:7].tolist(),
            dates[4:8]
        )
    ]

    instruments += [
        ForwardRateAgreement(
            discountCurve=initialCurve,
            fixedRate=rate,
            effectiveDate=startDate,
            terminationDate=endDate,
            frequency='1Y',
            endOfMonth=endOfMonth,
            businessDayConvention=businessDayConvention,
            dayCounter=dayCounter,
            stubPeriod=stubPeriod,
            calendar=calendar,
            notional=1.
        )
        for startDate, endDate, rate in zip(
            eoniaDataframe["StartDate"][7:12],
            eoniaDataframe["EndDate"][7:12],
            eoniaDataframe["Rate"][7:12]
        )
    ]

    instruments += [
        InterestRateSwap(
            discountCurve=initialCurve,
            fixedRate=rate,
            effectiveDate=startDate,
            terminationDate=endDate,
            fixFrequency='1Y',
            floatFrequency='1Y',
            endOfMonth=endOfMonth,
            businessDayConvention=businessDayConvention,
            dayCounter=dayCounter,
            stubPeriod=stubPeriod,
            calendar=calendar,
            notional=1.
        )
        for startDate, endDate, rate in zip(
            eoniaDataframe["StartDate"][12:],
            eoniaDataframe["EndDate"][12:],
            eoniaDataframe["Rate"][12:]
        )
    ]

    curve, convergenceStatus = CurveBootstrapping(
        initialGuessNodes=initialNodes,
        instruments=instruments,
        instrumentsQuotes=eoniaDataframe["Rate"].tolist(),
        dayCounter=dayCounter,
        curveInterpolator=LogLinearInterpolator
    ).solve()

    print(curve)
