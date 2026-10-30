from .StrEnum import StrEnum


class AiCoordinatorSeverityLevel(StrEnum):
    """Severity filter for auto-triage/auto-remediation eligibility."""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
