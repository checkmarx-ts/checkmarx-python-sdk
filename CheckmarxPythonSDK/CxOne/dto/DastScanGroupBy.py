from .StrEnum import StrEnum


class DastScanGroupBy(StrEnum):
    """Columns that DastScanAPI.get_scans_count_by_group can group by.

    Verified casings via the API's own validation error message —
    the doc's `riskrating` (all lowercase) is wrong; only `riskRating`
    is accepted.
    """
    INITIATOR = "initiator"
    SCAN_TYPE = "scantype"
    PROJECT_ID = "projectId"
    RISK_RATING = "riskRating"
