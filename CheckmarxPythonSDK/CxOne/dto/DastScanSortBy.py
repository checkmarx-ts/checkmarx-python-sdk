from .StrEnum import StrEnum


class DastScanSortBy(StrEnum):
    """Columns that DastScanAPI.get_scans can sort by."""
    INITIATOR = "initiator"
    SCAN_TYPE = "scantype"
    CREATED = "created"
    START_TIME = "starttime"
    UPDATE_TIME = "updatetime"
    SCAN_DURATION = "scanduration"
    LAST_STATUS = "laststatus"
    RISK_RATING = "riskrating"
