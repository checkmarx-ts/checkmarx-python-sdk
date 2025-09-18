from dataclasses import dataclass


@dataclass
class ScanInfo:
    """

    Attributes:
        scan_id (str):
        project_id (str):
        loc (int):
        file_count (int):
        is_incremental (bool):
        is_incremental_canceled (bool):
        incremental_cancel_reason (str):
        based_id (str):
        added_files_count (int):
        changed_files_count (int):
        deleted_files_count (int):
        change_percentage (float):
        query_preset (str):
    """

    scan_id: str
    project_id: str
    loc: int
    file_count: int
    is_incremental: bool
    is_incremental_canceled: bool
    incremental_cancel_reason: str
    based_id: str
    added_files_count: int
    changed_files_count: int
    deleted_files_count: int
    change_percentage: float
    query_preset: str


def construct_scan_info(item):
    return ScanInfo(
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
        query_preset=item.get("queryPreset")
    )
