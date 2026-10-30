from .StrEnum import StrEnum


class AiCoordinatorRiskStatus(StrEnum):
    """Finding occurrence status, used as an auto-triage/auto-remediation
    eligibility filter."""
    NEW = "NEW"
    RECURRENT = "RECURRENT"
