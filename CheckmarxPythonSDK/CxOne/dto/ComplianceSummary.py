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
