from dataclasses import dataclass
from typing import Optional


@dataclass
class DastComplianceData:
    """The `compliance` field on a ScansOverTime entry.

    `compliance_breakdown` is left as a raw dict -- its ComplianceBreakdown
    schema wasn't explored, and this nested a level deeper than is worth
    modeling for a rarely-needed overview metric.
    """
    total_risks: Optional[int] = None
    compliance_coverage_percentage: Optional[float] = None
    compliance_breakdown: Optional[dict] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastComplianceData":
        return cls(
            total_risks=item.get("total_risks"),
            compliance_coverage_percentage=item.get("compliance_coverage_percentage"),
            compliance_breakdown=item.get("compliance_breakdown"),
        )
