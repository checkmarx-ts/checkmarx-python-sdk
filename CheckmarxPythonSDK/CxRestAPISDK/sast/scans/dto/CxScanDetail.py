# encoding: utf-8
from dataclasses import dataclass
from typing import Optional


@dataclass
class CxScanDetail:
    """ """

    id: Optional[int] = None
    project: Optional[object] = None
    status: Optional[object] = None
    scan_type: Optional[object] = None
    comment: Optional[str] = None
    date_and_time: Optional[object] = None
    results_statistics: Optional[object] = None
    scan_state: Optional[object] = None
    owner: Optional[str] = None
    origin: Optional[str] = None
    origin_url: Optional[str] = None
    initiator_name: Optional[str] = None
    owning_team_id: Optional[int] = None
    is_public: Optional[bool] = None
    is_locked: Optional[bool] = None
    is_incremental: Optional[bool] = None
    scan_risk: Optional[int] = None
    scan_risk_severity: Optional[int] = None
    engine_server: Optional[object] = None
    finished_scan_status: Optional[object] = None
    partial_scan_reasons: Optional[object] = None
    custom_fields: Optional[object] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxScanDetail":
        from .CxStatus import CxStatus
        from .CxStatusDetail import CxStatusDetail
        from .CxScanType import CxScanType
        from .CxDateAndTime import CxDateAndTime
        from .CxResultsStatistics import CxResultsStatistics
        from .CxScanState import CxScanState
        from .CxLanguageState import CxLanguageState
        from .CxFinishedScanStatus import CxFinishedScanStatus

        project_dict = item.get("project") or {}
        status_dict = item.get("status") or {}
        scan_type_dict = item.get("scanType") or {}
        date_dict = item.get("dateAndTime") or {}
        results_stats_dict = item.get("resultsStatistics") or {}
        scan_state_dict = item.get("scanState") or {}
        engine_server_dict = item.get("engineServer") or {}
        finished_scan_status_dict = item.get("finishedScanStatus") or {}

        return cls(
            id=item.get("id"),
            project=project_dict,
            status=CxStatus.from_dict(status_dict),
            scan_type=CxScanType.from_dict(scan_type_dict),
            comment=item.get("comment"),
            date_and_time=CxDateAndTime.from_dict(date_dict),
            results_statistics=CxResultsStatistics.from_dict(results_stats_dict),
            scan_state=CxScanState.from_dict(scan_state_dict),
            owner=item.get("owner"),
            origin=item.get("origin"),
            origin_url=item.get("originURL"),
            initiator_name=item.get("initiatorName"),
            owning_team_id=item.get("owningTeamId"),
            is_public=item.get("isPublic"),
            is_locked=item.get("isLocked"),
            is_incremental=item.get("isIncremental"),
            scan_risk=item.get("scanRisk"),
            scan_risk_severity=item.get("scanRiskSeverity"),
            engine_server=engine_server_dict,
            finished_scan_status=CxFinishedScanStatus.from_dict(
                finished_scan_status_dict
            ),
            partial_scan_reasons=item.get("partialScanReasons"),
            custom_fields=item.get("customFields"),
        )
