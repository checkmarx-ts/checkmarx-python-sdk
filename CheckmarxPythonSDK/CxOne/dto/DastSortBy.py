from .StrEnum import StrEnum


class DastSortBy(StrEnum):
    """Columns that DastScanAPI.get_environments can sort by."""
    DOMAIN = "domain"
    URL = "url"
    SCAN_TYPE = "scantype"
    LAST_SCAN_TIME = "lastscantime"
    LAST_SCAN_STATUS = "lastscanstatus"
    LAST_RISK_RATING = "lastriskrating"
    CREATED = "created"
    AUTH_SUCCESS = "authsuccess"
