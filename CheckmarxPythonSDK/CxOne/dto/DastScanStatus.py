from .StrEnum import StrEnum


class DastScanStatus(StrEnum):
    """Documented values for the `lastStatus` filter parameter of
    GET /api/dast/scans/scans. The response field of the same name has
    been observed to contain values outside this set (e.g. "Completed"),
    so callers should treat the response as Union[DastScanStatus, str].
    """
    NEW = "New"
    EXTERNAL_SCAN = "ExternalScan"
    RUNNING = "Running"
    FINISHED = "Finished"
    FAILED = "Failed"
    CANCELLED = "Cancelled"
