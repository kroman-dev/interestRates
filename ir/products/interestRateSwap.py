from datetime import date
from typing import Optional

from ir.legs.fixedLeg import FixedLeg
from ir.legs.floatingLeg import FloatingLeg
from ir.products.bootstrapInstrument import BootstrapInstrument
from ir.products.swap import Swap
from ir.curve.genericCurve import GenericCurve
from ir.dayCounter.genericDayCounter import GenericDayCounter
from ir.scheduler.calendar.genericCalendar import GenericCalendar
from ir.scheduler.businessDayConvention.genericBusinessDayConvention import \
    GenericBusinessDayConvention
from ir.scheduler.schedule.schedule import Schedule
from ir.scheduler.stubPeriod.genericStubPeriod import GenericStubPeriod


class InterestRateSwap(Swap):
    """
        Vanilla IRS
    """
    def __init__(
            self,
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
            discountCurve: GenericCurve,
            forwardCurve: Optional[GenericCurve] = None,
            notional: float = 1,
            paymentLag: int = 0,
            floatLegDayCounter: Optional[GenericDayCounter] = None
    ):
        # TODO add roll day
        # TODO add leg2 params
        super().__init__(
            receiveLeg=FloatingLeg(
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
                dayCounter=dayCounter if floatLegDayCounter is None
                    else floatLegDayCounter,
                notional=notional,
                discountCurve=discountCurve,
                forwardCurve=forwardCurve
            ),
            payLeg=FixedLeg(
                fixedRate=fixedRate,
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
                dayCounter=dayCounter,
                notional=notional,
                discountCurve=discountCurve,
                forwardCurve=forwardCurve
            )
        )
