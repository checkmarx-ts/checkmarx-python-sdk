from dataclasses import dataclass


@dataclass
class ScanInfo:
    scan_id: str = None
    project_id: str = None
    loc: int = None
    file_count: int = None
    is_incremental: bool = None
    is_incremental_canceled: bool = None
    incremental_cancel_reason: str = None
    based_id: str = None
    added_files_count: int = None
    changed_files_count: int = None
    deleted_files_count: int = None
    change_percentage: float = None
    query_preset: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "ScanInfo":
        return cls(
            scan_id=item.get("scanId"),
            project_id=item.get("projectId"),
            loc=item.get("loc"),
            file_count=item.get("fileCount"),
            is_incremental=item.get("isIncremental"),
            is_incremental_canceled=item.get("isIncrementalCanceled"),
            incremental_cancel_reason=item.get("incrementalCancelReason"),
            based_id=item.get("baseId"),
            added_files_count=item.get("addedFilesCount"),
            changed_files_count=item.get("changedFilesCount"),
            deleted_files_count=item.get("deletedFilesCount"),
            change_percentage=item.get("changePercent"),
            query_preset=item.get("queryPreset"),
        )
