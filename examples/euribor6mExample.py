import os
import datetime
import pandas as pd

from ir import *
from examples.eoniaExample import bootstrapEonia
from ir.index.euribor6m import Euribor6M
from ir.products.indexForwardRateAgreement import IndexForwardRateAgreement

if __name__ == '__main__':
    discountCurve = bootstrapEonia()
    euribor6m = Euribor6M()

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
    dates = [spotDate] + [euriborDataframe["StartDate"].tolist()[0]] \
            + euriborDataframe["EndDate"].tolist()

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
            euriborDataframe["StartDate"][:10],
            euriborDataframe["EndDate"][:10],
            euriborDataframe["Rate"][:10]
        )
    ]

    initialNodes = {_date: 1 for _date in dates}
    initialCurve = DiscountCurve(
        dates=list(initialNodes.keys()),
        discountFactors=list(initialNodes.values()),
        dayCounter=euribor6m.getDayCounter()
    )
    curve, convergenceStatus = CurveBootstrapping(
        initialGuessNodes=initialNodes,
        instruments=instruments,
        instrumentsQuotes=euriborDataframe["Rate"][:10],
        dayCounter=dayCounter,
        curveInterpolator=LogLinearInterpolator
    ).solve()
