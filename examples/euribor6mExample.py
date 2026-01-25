import os
import datetime
import pandas as pd

from ir import *
from examples.eoniaExample import bootstrapEonia
from ir.index.euribor6m import Euribor6M
from ir.products.indexForwardRateAgreement import IndexForwardRateAgreement
from ir.products.indexInterestRateSwap import IndexInterestRateSwap


if __name__ == '__main__':
    euribor6m = Euribor6M()
    discountCurve = bootstrapEonia()
    discountCurve.setEnableExtrapolation(True)

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

    curve, convergenceStatus = CurveBootstrapping(
        initialGuessNodes={_date: 1 for _date in dates},
        instruments=instruments,
        instrumentsQuotes=euriborDataframe["Rate"],
        dayCounter=euribor6m.getDayCounter(),
        discountCurve=discountCurve.convertToFloatValues()
    ).solve()

    print(curve)
