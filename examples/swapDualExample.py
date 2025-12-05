from datetime import date

from ir.curve.discountCurve import DiscountCurve
from ir.dayCounter.act365Fixed import Act365Fixed
from ir.dualNumbers.dualNumber import DualNumber
from ir.legs.fixedLeg import FixedLeg
from ir.legs.floatingLeg import FloatingLeg
from ir.products.interestRateSwap import InterestRateSwap
from ir.products.swap import Swap
from ir.scheduler.businessDayConvention.noConvention import NoConvention
from ir.scheduler.calendar.noCalendar import NoCalendar
from ir.scheduler.schedule.schedule import Schedule
from ir.scheduler.stubPeriod.shortBack import ShortBack


if __name__ == '__main__':
    
        dayCounter = Act365Fixed
        effectiveDate = date(2022, 2, 14)
        terminationDate = date(2022, 6, 14)
        businessDayConvention = NoConvention()
        calendar = NoCalendar()
        stubPeriod = ShortBack()

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

        swap = Swap(
            receiveLeg=FloatingLeg(
                curve=curve,
                schedule=Schedule(
                    effectiveDate=effectiveDate,
                    terminationDate=terminationDate,
                    frequency='1M',
                    businessDayConvention=businessDayConvention,
                    endOfMonth=False,
                    stubPeriod=stubPeriod,
                    calendar=calendar,
                    paymentLag=0
                ),
                businessDayConvention=businessDayConvention,
                dayCounter=dayCounter
            ),
            payLeg=FixedLeg(
                fixedRate=1.15 / 100,
                curve=curve,
                schedule=Schedule(
                    effectiveDate=effectiveDate,
                    terminationDate=terminationDate,
                    frequency='4M',
                    businessDayConvention=businessDayConvention,
                    endOfMonth=False,
                    stubPeriod=stubPeriod,
                    calendar=calendar,
                    paymentLag=0
                ),
                businessDayConvention=businessDayConvention,
                dayCounter=dayCounter
            )
        )
        notional = 1e9
        print(swap.npv() * notional)

        print(
            InterestRateSwap(
                curve=curve,
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
            ).npv()
        )
