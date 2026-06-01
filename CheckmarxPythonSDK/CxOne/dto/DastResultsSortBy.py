from .StrEnum import StrEnum


class DastResultsSortBy(StrEnum):
    """Columns that DastResultsAPI.get_results can sort by."""
    STATUS = "status"
    NAME = "name"
    URL = "url"
    METHOD = "method"
    SCAN_TYPE = "scan_type"
    SEVERITY = "severity"
    STATE = "state"
    PATH = "path"
