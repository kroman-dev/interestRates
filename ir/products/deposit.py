from datetime import date
from typing import Optional

from ir.products.bootstrapInstrument import BootstrapInstrument
from ir.scheduler.period.period import Period
from ir.curve.genericCurve import GenericCurve
from ir.dayCounter.genericDayCounter import GenericDayCounter
from ir.products.legs.fixedLeg import FixedLeg
from ir.scheduler.businessDayConvention.genericBusinessDayConvention import \
    GenericBusinessDayConvention
from ir.scheduler.calendar.genericCalendar import GenericCalendar
from ir.scheduler.schedule.schedule import Schedule
from ir.scheduler.stubPeriod.genericStubPeriod import GenericStubPeriod


class Deposit(BootstrapInstrument):
    """
        Uncollateralized, so only one curve as input
    """
    def __init__(
            self,
            fixedRate: float,
            effectiveDate: date,
            tenor: str,
            businessDayConvention: GenericBusinessDayConvention,
            endOfMonth: bool,
            dayCounter: GenericDayCounter,
            stubPeriod: GenericStubPeriod,
            calendar: GenericCalendar,
            notional: float = 1.,
            curve: Optional[GenericCurve] = None,
    ):
        self._fixedLeg = FixedLeg(
            fixedRate=fixedRate,
            schedule=Schedule(
                effectiveDate=effectiveDate,
                terminationDate=calendar.advance(
                    date=effectiveDate,
                    period=Period(tenor),
                    businessDayConvention=businessDayConvention,
                    endOfMonth=endOfMonth
                ),
                frequency=tenor,
                businessDayConvention=businessDayConvention,
                endOfMonth=endOfMonth,
                stubPeriod=stubPeriod,
                calendar=calendar,
                paymentLag=0
            ),
            dayCounter=dayCounter,
            notional=notional,
            discountCurve=curve
        )

    def npv(
            self,
            discountCurve: Optional[GenericCurve] = None,
            forwardCurve: Optional[GenericCurve] = None
    ) -> float:
        raise self._fixedLeg.npv(
            discountCurve=discountCurve,
            forwardCurve=forwardCurve
        )

    def getParRate(
            self,
            discountCurve: Optional[GenericCurve] = None,
            forwardCurve: Optional[GenericCurve] = None
    ) -> float:
        # Deposit is not a collateralized contract, so we prefer forwardCurve
        if forwardCurve is not None:
            discountCurve = forwardCurve
        scheduleData = self._fixedLeg.getSchedule().getSchedule()
        if len(scheduleData.accrualStartDates) > 1:
            raise ValueError('Incorrect schedule')
        if discountCurve is None:
            discountCurve = self._fixedLeg.getDiscountCurve()
        return 1 / self._fixedLeg.getAccruals()[0] * (
            discountCurve.getDiscountFactor(
                scheduleData.accrualStartDates[0]
            ) / discountCurve.getDiscountFactor(
                scheduleData.paymentDates[0]
            ) - 1
        )
