from datetime import date
from typing import Optional

from ir.products.legs.floatingLeg import FloatingLeg
from ir.products.swap import Swap
from ir.curve.genericCurve import GenericCurve
from ir.dayCounter.genericDayCounter import GenericDayCounter
from ir.products.legs.fixedLeg import FixedLeg
from ir.scheduler.businessDayConvention.genericBusinessDayConvention import \
    GenericBusinessDayConvention
from ir.scheduler.calendar.genericCalendar import GenericCalendar
from ir.scheduler.schedule.schedule import Schedule
from ir.scheduler.stubPeriod.genericStubPeriod import GenericStubPeriod


class ForwardRateAgreement(Swap):
    """
        For typical post credit crunch market situations,
         the actual size of the convexity adjustment results to be below 1 bp,
          even for long maturities. Hence, in any practical situation,
           we can discard the convexity adjustment and use the classical
            pricing expressions [1].
        Ref:
        [1] Ametrano, Ferdinando M., and Marco Bianchetti.
         Everything you always wanted to know about multiple interest rate
          curve bootstrapping but were afraid to ask. Vol. 2219548. SSRN, 2013.
    """
    def __init__(
            self,
            fixedRate: float,
            effectiveDate: date,
            terminationDate: date,
            frequency: str,
            endOfMonth: bool,
            businessDayConvention: GenericBusinessDayConvention,
            dayCounter: GenericDayCounter,
            stubPeriod: GenericStubPeriod,
            calendar: GenericCalendar,
            discountCurve: Optional[GenericCurve] = None,
            forwardCurve: Optional[GenericCurve] = None,
            notional: float = 1,
            paymentLag: int = 0
    ):
        schedule = Schedule(
            effectiveDate=effectiveDate,
            terminationDate=terminationDate,
            frequency=frequency,
            businessDayConvention=businessDayConvention,
            endOfMonth=endOfMonth,
            stubPeriod=stubPeriod,
            calendar=calendar,
            paymentLag=paymentLag
        )
        if len(schedule.getSchedule().paymentDates) > 1:
            raise ValueError('Incorrect schedule was created')
        super().__init__(
            receiveLeg=FloatingLeg(
                schedule=schedule,
                dayCounter=dayCounter,
                notional=notional,
                discountCurve=discountCurve,
                forwardCurve=forwardCurve
            ),
            payLeg=FixedLeg(
                fixedRate=fixedRate,
                schedule=schedule,
                dayCounter=dayCounter,
                notional=notional,
                discountCurve=discountCurve,
                forwardCurve=forwardCurve
            )
        )
