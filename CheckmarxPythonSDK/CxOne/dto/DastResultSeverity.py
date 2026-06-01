from .StrEnum import StrEnum


class DastResultSeverity(StrEnum):
    """Allowed severity values for the changelog update."""
    INFO = "INFO"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"
