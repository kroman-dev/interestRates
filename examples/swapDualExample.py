from datetime import date

from ir.curve.discountCurve import DiscountCurve
from ir.dayCounter.act365Fixed import Act365Fixed
from ir.dualNumbers.dualNumber import DualNumber
from ir.products.interestRateSwap import InterestRateSwap
from ir.scheduler.businessDayConvention.noConvention import NoConvention
from ir.scheduler.calendar.noCalendar import NoCalendar
from ir.scheduler.stubPeriod.shortBack import ShortBack

if __name__ == '__main__':
    dayCounter = Act365Fixed
    effectiveDate = date(2022, 2, 14)
    terminationDate = date(2022, 6, 14)
    businessDayConvention = NoConvention()
    calendar = NoCalendar()
    stubPeriod = ShortBack()
    notional = 1e9

    bpScale = 1e-4
    curve = DiscountCurve(
        dates=[date(2022, 1, 1), date(2022, 4, 1), date(2022, 7, 1)],
        discountFactors=[
            DualNumber(1., {"p0": 1}),
            DualNumber(
                0.9975,
                {
                    "p1": 1,
                    'r1': -0.9975 * bpScale * dayCounter.yearFraction(
                        date(2022, 1, 1),
                        date(2022, 4, 1)
                    )
                }
            ),
            DualNumber(
                0.9945, {
                    "p2": 1,
                    'r2': -0.9945 * bpScale * dayCounter.yearFraction(
                        date(2022, 1, 1),
                        date(2022, 7, 1)
                    )
                }
            )
        ],
        dayCounter=dayCounter
    )

    sampleSwap = InterestRateSwap(
        fixedRate=1.15 / 100,
        effectiveDate=effectiveDate,
        terminationDate=terminationDate,
        fixFrequency='4M',
        floatFrequency='1M',
        endOfMonth=False,
        businessDayConvention=businessDayConvention,
        dayCounter=dayCounter,
        stubPeriod=stubPeriod,
        calendar=calendar,
        notional=notional
    )
    print(sampleSwap.npv(curve))
    print()
    print(sampleSwap.getParRate(curve))

    eps = 1e-7
    curveTest = DiscountCurve(
        dates=[date(2022, 1, 1), date(2022, 4, 1), date(2022, 7, 1)],
        discountFactors=[1., 0.9975 + eps, 0.9945],
        dayCounter=dayCounter
    )

    print((sampleSwap.npv(curveTest) - sampleSwap.npv(curve).realPart) / eps)
