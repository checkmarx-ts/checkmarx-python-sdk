from dataclasses import dataclass
from typing import List, Optional

from .Query import Query


@dataclass
class CxXMLResults:
    initiator_name: Optional[str] = None
    owner: Optional[str] = None
    scan_id: Optional[int] = None
    project_id: Optional[int] = None
    project_name: Optional[str] = None
    team_full_path_on_report_date: Optional[str] = None
    deep_link: Optional[str] = None
    scan_start: Optional[str] = None
    preset: Optional[str] = None
    scan_time: Optional[str] = None
    lines_of_code_scanned: Optional[int] = None
    files_scanned: Optional[int] = None
    report_creation_time: Optional[str] = None
    team: Optional[str] = None
    checkmarx_version: Optional[str] = None
    scan_comments: Optional[str] = None
    scan_type: Optional[str] = None
    source_origin: Optional[str] = None
    visibility: Optional[str] = None
    queries: Optional[List[Query]] = None

    @classmethod
    def from_dict(cls, item: dict, queries=None) -> "CxXMLResults":
        return cls(
            initiator_name=item.get("InitiatorName"),
            owner=item.get("Owner"),
            scan_id=int(item.get("ScanId")),
            project_id=int(item.get("ProjectId")),
            project_name=item.get("ProjectName"),
            team_full_path_on_report_date=item.get("TeamFullPathOnReportDate"),
            deep_link=item.get("DeepLink"),
            scan_start=item.get("ScanStart"),
            preset=item.get("Preset"),
            scan_time=item.get("ScanTime"),
            lines_of_code_scanned=int(item.get("LinesOfCodeScanned")),
            files_scanned=int(item.get("FilesScanned")),
            report_creation_time=item.get("ReportCreationTime"),
            team=item.get("Team"),
            checkmarx_version=item.get("CheckmarxVersion"),
            scan_comments=item.get("ScanComments"),
            scan_type=item.get("ScanType"),
            source_origin=item.get("SourceOrigin"),
            visibility=item.get("Visibility"),
            queries=queries,
        )
