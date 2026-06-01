from .StrEnum import StrEnum


class DastGroupBy(StrEnum):
    """Columns that DastScanAPI.get_environments_count_by_group can
    group by. The API accepts both scanType and scantype; we send
    the lowercase form (verified working against the live API)."""
    DOMAIN = "domain"
    URL = "url"
    SCAN_TYPE = "scantype"
    LAST_RISK_RATING = "lastRiskRating"
    PROJECT_IDS = "projectIds"
