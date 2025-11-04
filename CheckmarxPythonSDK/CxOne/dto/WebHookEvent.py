from .StrEnum import StrEnum


class WebHookEvent(StrEnum):
    SCAN_COMPLETED = "scan_completed_successfully"
    SCAN_FAILED = "scan_failed"
    SCAN_PARTIAL = "scan_partial"
    PROJECT_CREATED = "project_created"
