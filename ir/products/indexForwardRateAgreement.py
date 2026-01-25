from datetime import date
from typing import Optional

from ir.products.forwardRateAgreement import ForwardRateAgreement
from ir.curve.genericCurve import GenericCurve
from ir.dayCounter.genericDayCounter import GenericDayCounter
from ir.index.index import Index
from ir.scheduler.stubPeriod.genericStubPeriod import GenericStubPeriod


class IndexForwardRateAgreement(ForwardRateAgreement):
    """
        Forward Rate Agreement that uses an Index to set parameters
    """
    def __init__(
            self,
            index: Index,
            fixedRate: float,
            effectiveDate: date,
            terminationDate: date,
            stubPeriod: GenericStubPeriod,
            dayCounter: Optional[GenericDayCounter] = None,
            discountCurve: Optional[GenericCurve] = None,
            forwardCurve: Optional[GenericCurve] = None,
            notional: float = 1,
            paymentLag: int = 0,
    ):
        super().__init__(
            fixedRate=fixedRate,
            effectiveDate=effectiveDate,
            terminationDate=terminationDate,
            frequency=index.getTenor(),
            endOfMonth=index.getEndOfMonth(),
            businessDayConvention=index.getBusinessDayConvention(),
            dayCounter=index.getDayCounter() if dayCounter is None else dayCounter,
            stubPeriod=stubPeriod,
            calendar=index.getCalendar(),
            discountCurve=discountCurve,
            forwardCurve=forwardCurve,
            notional=notional,
            paymentLag=paymentLag
        )
