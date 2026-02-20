import os
import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from ir import *
from ir.index.euribor6m import Euribor6M
from ir.products.indexForwardRateAgreement import IndexForwardRateAgreement
from ir.products.indexInterestRateSwap import IndexInterestRateSwap
from examples.eoniaExample import bootstrapEonia


def getEuribor6mDataframe() -> pd.DataFrame:
    mainDir = os.path.dirname(os.path.abspath(""))
    euriborDataframe = pd.read_csv(
        os.path.abspath(os.path.join(mainDir, "data/euribor6m11122012.csv")),
        sep=';'
    )
    euriborDataframe['StartDate'] = euriborDataframe['Start Date'].apply(
        lambda x: datetime.datetime.strptime(x, '%a %d %b %Y').date()
    )
    euriborDataframe['EndDate'] = euriborDataframe['End Date'].apply(
        lambda x: datetime.datetime.strptime(x, '%a %d %b %Y').date()
    )
    euriborDataframe['Rate'] = euriborDataframe['Rate, %'] / 100
    # delete synthetic instruments
    euriborDataframe = euriborDataframe.iloc[9:].reset_index(drop=True)
    return euriborDataframe


if __name__ == '__main__':
    euribor6m = Euribor6M()
    discountCurve = bootstrapEonia()
    discountCurve.setEnableExtrapolation(True)
    euriborDataframe = getEuribor6mDataframe()

    todayDate = datetime.date(2012, 12, 11)
    spotDate = todayDate + Period('2D')
    fraEndIndex = 19
    dates = [spotDate] + euriborDataframe["EndDate"].tolist()[:]

    stubPeriod = ShortBack()

    instruments = [
        IndexForwardRateAgreement(
            index=euribor6m,
            fixedRate=rate,
            effectiveDate=startDate,
            terminationDate=endDate,
            stubPeriod=stubPeriod
        )
        for startDate, endDate, rate in zip(
            euriborDataframe["StartDate"][:fraEndIndex],
            euriborDataframe["EndDate"][:fraEndIndex],
            euriborDataframe["Rate"][:fraEndIndex]
        )
    ]
    instruments += [
        IndexInterestRateSwap(
            index=euribor6m,
            fixedRate=rate,
            effectiveDate=startDate,
            terminationDate=endDate,
            fixFrequency='1Y',
            stubPeriod=stubPeriod,
            dayCounter=Thirty360BondBasis()
        )
        for startDate, endDate, rate in zip(
            euriborDataframe["StartDate"][fraEndIndex:],
            euriborDataframe["EndDate"][fraEndIndex:],
            euriborDataframe["Rate"][fraEndIndex:]
        )
    ]

    curve, convergenceStatus = BootstrappingSolver(
        initialGuessNodes={_date: 1 for _date in dates},
        instruments=instruments,
        instrumentsQuotes=euriborDataframe["Rate"],
        dayCounter=euribor6m.getDayCounter(),
        discountCurve=discountCurve.convertToFloatValues()
    ).solve()

    print(curve)

    curve.setEnableExtrapolation(True)
    datesForPlot = np.arange(dates[0], dates[-1]).tolist()

    forwardRates = [
        curve.getForwardRate(
            periodStart=startDate,
            periodEnd=startDate+Period(euribor6m.getTenor())
        ).realPart
        for startDate in datesForPlot
    ]
    plt.plot(datesForPlot,forwardRates)
    plt.show()
