from datetime import date
from typing import Optional

from ir.scheduler.period.period import Period
from ir.curve.discountCurve import DiscountCurve
from ir.dayCounter.genericDayCounter import GenericDayCounter
from ir.legs.fixedLeg import FixedLeg
from ir.scheduler.businessDayConvention.genericBusinessDayConvention import \
    GenericBusinessDayConvention
from ir.scheduler.calendar.genericCalendar import GenericCalendar
from ir.scheduler.schedule.schedule import Schedule
from ir.scheduler.stubPeriod.genericStubPeriod import GenericStubPeriod


# TODO add abstract class
class Deposit:

    def __init__(
            self,
            curve: DiscountCurve,
            fixedRate: float,
            effectiveDate: date,
            tenor: str,
            businessDayConvention: GenericBusinessDayConvention,
            endOfMonth: bool,
            dayCounter: GenericDayCounter,
            stubPeriod: GenericStubPeriod,
            calendar: GenericCalendar,
            notional: float = 1.
    ):
        self._fixLeg = FixedLeg(
            fixedRate=fixedRate,
            curve=curve,
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
            businessDayConvention=businessDayConvention,
            dayCounter=dayCounter,
            notional=notional
        )

    def npv(self, curve: Optional[DiscountCurve] = None) -> float:
        return self._fixLeg._notional

    def getFixRate(self) -> float:
        return self._fixLeg.getFixRate()

    def getParRate(self, curve: Optional[DiscountCurve] = None) -> float:
        # TODO add raise if len bigger than 1
        return 1 / self._fixLeg._accrualYearFractions[0] * (
            curve.getDiscountFactor(
                # be more accurate -> look at article and refactor
                self._fixLeg._scheduleData.accrualStartDates[0]
            ) / curve.getDiscountFactor(
                self._fixLeg._scheduleData.paymentDates[0]
            ) - 1
        )
