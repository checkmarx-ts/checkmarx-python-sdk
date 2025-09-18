from dataclasses import dataclass


@dataclass
class ComplianceSummary:
    """

    Attributes:
        compliance (str):
        count (int):
    """
    compliance: str
    count: int


def construct_compliance_summary(item):
    return ComplianceSummary(
        compliance=item.get("compliance"),
        count=item.get("count")
    )
