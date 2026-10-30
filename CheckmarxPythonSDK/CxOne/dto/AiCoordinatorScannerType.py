from .StrEnum import StrEnum


class AiCoordinatorScannerType(StrEnum):
    """Scanner types supported by the AI Agents Coordinator (auto-triage/
    auto-remediation configuration filters)."""
    SAST = "SAST"
    SCA = "SCA"
