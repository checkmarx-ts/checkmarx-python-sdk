from .StrEnum import StrEnum


class DastResultStatus(StrEnum):
    """Documented values for DastResult.status."""
    NEW = "New"
    RECURRENT = "Recurrent"
