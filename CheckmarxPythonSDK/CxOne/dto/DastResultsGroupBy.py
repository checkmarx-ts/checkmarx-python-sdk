from .StrEnum import StrEnum


class DastResultsGroupBy(StrEnum):
    """Columns that DastResultsAPI.get_results_count_by_group can group by."""
    STATUS = "status"
    NAME = "name"
    METHOD = "method"
    SEVERITY = "severity"
    URL = "url"
    PATH = "path"
    STATE = "state"
    COMPLIANCE = "compliance"
    OWASP = "owasp"
