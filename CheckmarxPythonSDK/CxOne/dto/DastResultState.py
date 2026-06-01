from .StrEnum import StrEnum


class DastResultState(StrEnum):
    """Documented values for DastResult.state. Note the wire values
    include spaces (e.g. "To Verify"), not snake_case or PascalCase."""
    TO_VERIFY = "To Verify"
    NOT_EXPLOITABLE = "Not Exploitable"
    PROPOSED_NOT_EXPLOITABLE = "Proposed Not Exploitable"
    CONFIRMED = "Confirmed"
    URGENT = "Urgent"
