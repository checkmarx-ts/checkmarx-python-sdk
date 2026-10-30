from .StrEnum import StrEnum


class AiCoordinatorRiskState(StrEnum):
    """Engine-resolved triage verdict (predicate state). Used as an
    auto-remediation eligibility filter -- auto-triage has no riskState
    filter since it's the one setting this state."""
    TO_VERIFY = "TO_VERIFY"
    CONFIRMED = "CONFIRMED"
    URGENT = "URGENT"
    PROPOSED_NOT_EXPLOITABLE = "PROPOSED_NOT_EXPLOITABLE"
    NOT_EXPLOITABLE = "NOT_EXPLOITABLE"
