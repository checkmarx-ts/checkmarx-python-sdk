from dataclasses import dataclass
from typing import Optional


@dataclass
class ScaExportStatus:
    """Response from GET /api/sca/export/requests?exportId={exportId}
    -- status and download link for an SCA export request created via
    ReportAPI.create_sca_scan_report.
    """
    export_id: Optional[str] = None
    export_status: Optional[str] = None  # Pending, Exporting, Completed, Failed
    file_url: Optional[str] = None  # only set when export_status is Completed
    error_message: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "ScaExportStatus":
        return cls(
            export_id=item.get("exportId"),
            export_status=item.get("exportStatus"),
            file_url=item.get("fileUrl"),
            error_message=item.get("errorMessage"),
        )
