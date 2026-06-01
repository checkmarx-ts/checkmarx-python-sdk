from .StrEnum import StrEnum


class DastScanOption(StrEnum):
    """Allowed values for settings.scanOptions.scanOption."""
    FAST = "fast"
    BALANCED = "balanced"
    DEEP = "deep"
    THOROUGH = "thorough"
