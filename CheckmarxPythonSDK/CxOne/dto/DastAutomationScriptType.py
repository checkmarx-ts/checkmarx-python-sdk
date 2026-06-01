from .StrEnum import StrEnum


class DastAutomationScriptType(StrEnum):
    """Allowed values for automationScripts[].scriptType."""
    HTTP_SENDER = "httpsender"
    ACTIVE = "active"
    PASSIVE = "passive"
    VARIANT = "variant"
    SELENIUM = "selenium"
