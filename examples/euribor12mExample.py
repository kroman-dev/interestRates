import os
import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from ir import *
from ir.index.euribor12m import Euribor12M
from ir.products.indexForwardRateAgreement import IndexForwardRateAgreement
from ir.products.indexInterestRateSwap import IndexInterestRateSwap

from examples.eoniaExample import bootstrapEonia
from examples.euribor6mExample import getEuribor6mDataframe


def getEurBasisDataframe() -> pd.DataFrame:
    mainDir = os.path.dirname(os.path.abspath(""))
    eurIrsbDataframe = pd.read_csv(
        os.path.abspath(os.path.join(mainDir, "data/eurBasisSwaps11122012.csv")),
        sep=';'
    )
    eurIrsbDataframe = eurIrsbDataframe.drop(
        columns=["Quote (bid. %)", "Quote (ask. %)"]
    )
    eurIrsbDataframe['StartDate'] = eurIrsbDataframe['Start Date'].apply(
        lambda x: datetime.datetime.strptime(x, '%a %d %b %Y').date()
    )
    eurIrsbDataframe['EndDate'] = eurIrsbDataframe['Maturity Date'].apply(
        lambda x: datetime.datetime.strptime(x, '%a %d %b %Y').date()
    )
    eurIrsbDataframe['Basis'] = eurIrsbDataframe['Quote (mid. %)'] / 10000

    e6e12BasisDataframe = eurIrsbDataframe[
        eurIrsbDataframe["Underlying 2nd leg"] == "Euribor12M"
    ].reset_index(drop=True)
    return e6e12BasisDataframe


if __name__ == '__main__':
    euribor12m = Euribor12M()
    discountCurve = bootstrapEonia()
    discountCurve.setEnableExtrapolation(True)

    euribor6mDataframe = getEuribor6mDataframe().iloc[19:-4]
    e6e12BasisDataframe = getEurBasisDataframe().iloc[2:]
    e6e12BasisDataframe = e6e12BasisDataframe.drop(10)
    print(e6e12BasisDataframe)

    euribor12mDataframe = pd.DataFrame()
    euribor12mDataframe["StartDate"] = e6e12BasisDataframe["StartDate"]
    euribor12mDataframe["EndDate"] = e6e12BasisDataframe["EndDate"]
    euribor12mDataframe["Rate"] = e6e12BasisDataframe["Basis"].to_numpy() \
                                  + euribor6mDataframe["Rate"].to_numpy()

    todayDate = datetime.date(2012, 12, 11)
    spotDate = todayDate + Period('2D')
    stubPeriod = ShortBack()

    dates = [
        spotDate,
        datetime.date(2013, 12, 13), # deposit
        datetime.date(2014, 12, 15)  # fra
    ] + euribor12mDataframe["EndDate"].tolist()

    quotes = [0.54 / 100, 0.507 / 100] \
             + euribor12mDataframe["Rate"].tolist()

    instruments = [
        Deposit(
            fixedRate=0.54 / 100,
            effectiveDate=spotDate,
            tenor='1Y',
            endOfMonth=euribor12m.getEndOfMonth(),
            businessDayConvention=ModifiedFollowing(), # see fig 4.
            dayCounter=euribor12m.getDayCounter(),
            stubPeriod=stubPeriod,
            calendar=euribor12m.getCalendar(),
            notional=1.
        ),
        IndexForwardRateAgreement(
            index=euribor12m,
            fixedRate=0.507 / 100,
            effectiveDate=datetime.date(2013, 12, 13),
            terminationDate=datetime.date(2014, 12, 15),
            stubPeriod=stubPeriod
        )
    ]

    instruments += [
        IndexInterestRateSwap(
            index=euribor12m,
            fixedRate=rate,
            effectiveDate=startDate,
            terminationDate=endDate,
            fixFrequency='1Y',
            stubPeriod=stubPeriod,
            dayCounter=Thirty360BondBasis()
        )
        for startDate, endDate, rate in zip(
            euribor12mDataframe["StartDate"],
            euribor12mDataframe["EndDate"],
            euribor12mDataframe["Rate"]
        )
    ]

    curve, convergenceStatus = BootstrappingSolver(
        initialGuessNodes={_date: 1 for _date in dates},
        instruments=instruments,
        instrumentsQuotes=quotes,
        dayCounter=euribor12m.getDayCounter(),
        discountCurve=discountCurve.convertToFloatValues()
    ).solve()

    curve.setEnableExtrapolation(True)
    datesForPlot = np.arange(dates[0], dates[-1]).tolist()

    forwardRates = [
        curve.getForwardRate(
            periodStart=startDate,
            periodEnd=startDate+Period(euribor12m.getTenor())
        ).realPart
        for startDate in datesForPlot
    ]
    plt.plot(datesForPlot,forwardRates)
    plt.show()

