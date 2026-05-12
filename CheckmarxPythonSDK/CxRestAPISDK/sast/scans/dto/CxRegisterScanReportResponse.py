# encoding: utf-8
from dataclasses import dataclass
from typing import Optional


@dataclass
class CxRegisterScanReportResponse:
    """
    the response of register scan report
    """

    class Links:
        def __init__(self, report, status):
            """

            Args:
                report (:obj:`CxLink`):
                status (:obj:`CxLink`):
            """
            self.report = report
            self.status = status

    report_id: Optional[int] = None
    links: Optional[object] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxRegisterScanReportResponse":
        return cls(
            report_id=item.get("reportId"),
            links=item.get("links"),
        )
