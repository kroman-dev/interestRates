from datetime import date
from typing import Optional

from ir.legs.fixedLeg import FixedLeg
from ir.legs.floatingLeg import FloatingLeg
from ir.products.swap import Swap
from ir.curve.discountCurve import DiscountCurve
from ir.dayCounter.genericDayCounter import GenericDayCounter
from ir.scheduler.calendar.genericCalendar import GenericCalendar
from ir.scheduler.businessDayConvention.genericBusinessDayConvention import \
    GenericBusinessDayConvention
from ir.scheduler.schedule.schedule import Schedule
from ir.scheduler.stubPeriod.genericStubPeriod import GenericStubPeriod


class InterestRateSwap(Swap):
    """
        vanilla IRS
    """
    def __init__(
            self,
            curve: DiscountCurve,
            fixedRate: float,
            effectiveDate: date,
            terminationDate: date,
            fixFrequency: str,
            floatFrequency: str,
            endOfMonth: bool,
            businessDayConvention: GenericBusinessDayConvention,
            dayCounter: GenericDayCounter,
            stubPeriod: GenericStubPeriod,
            calendar: GenericCalendar,
            notional: float = 1,
            paymentLag: int = 0,
            floatLegDayCounter: Optional[GenericDayCounter] = None
    ):
        # TODO add roll day
        # TODO add leg2 params
        super().__init__(
            receiveLeg=FloatingLeg(
                curve=curve,
                schedule=Schedule(
                    effectiveDate=effectiveDate,
                    terminationDate=terminationDate,
                    frequency=floatFrequency,
                    businessDayConvention=businessDayConvention,
                    endOfMonth=endOfMonth,
                    stubPeriod=stubPeriod,
                    calendar=calendar,
                    paymentLag=paymentLag
                ),
                businessDayConvention=businessDayConvention,
                dayCounter=dayCounter if floatLegDayCounter is None
                    else floatLegDayCounter,
                notional=notional
            ),
            payLeg=FixedLeg(
                fixedRate=fixedRate,
                curve=curve,
                schedule=Schedule(
                    effectiveDate=effectiveDate,
                    terminationDate=terminationDate,
                    frequency=fixFrequency,
                    businessDayConvention=businessDayConvention,
                    endOfMonth=endOfMonth,
                    stubPeriod=stubPeriod,
                    calendar=calendar,
                    paymentLag=paymentLag
                ),
                businessDayConvention=businessDayConvention,
                dayCounter=dayCounter,
                notional=notional
            )
        )
