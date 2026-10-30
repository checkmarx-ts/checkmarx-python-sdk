from dataclasses import dataclass
from typing import Optional

from .DastTimeSpanRiskSummary import DastTimeSpanRiskSummary
from .RiskLevel import RiskLevel


@dataclass
class DastEnvironmentsRiskSummary:
    """Response from GET /envsRiskSummary/{appId}."""
    summarized_scan_risk: Optional[RiskLevel] = None
    span_summarized_scan_risk: Optional[DastTimeSpanRiskSummary] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastEnvironmentsRiskSummary":
        return cls(
            summarized_scan_risk=(
                RiskLevel.from_dict(item["SummerizedScanRisk"])
                if item.get("SummerizedScanRisk") else None
            ),
            span_summarized_scan_risk=(
                DastTimeSpanRiskSummary.from_dict(item["SpanSummerizedScanRisk"])
                if item.get("SpanSummerizedScanRisk") else None
            ),
        )
