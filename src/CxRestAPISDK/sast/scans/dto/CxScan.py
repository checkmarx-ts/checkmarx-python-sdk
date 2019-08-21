# encoding: utf-8


class CxScan(object):
    """

    """

    def __init__(self, id=None, project=None, status=None, scan_type=None, comment=None, date_and_time=None,
                 results_statistics=None, scan_state=None, owner=None, origin=None, initiator_name=None,
                 owning_team_id=None, is_public=None, is_locked=None, is_incremental=None, scan_risk=None,
                 scan_risk_severity=None, engine_server=None, finished_scan_status=None, partial_scan_reasons=None):
        """

        :param id: int
            scan id
        :param project: CxProject
        :param status: CxStatus
        :param scan_type: CxScanType
        :param comment: str
        :param date_and_time: CxDateAndTime
        :param results_statistics: CxResultsStatistics
        :param scan_state: CxScanState
        :param owner: str
        :param origin: str
        :param initiator_name: str
        :param owning_team_id: int
        :param is_public: boolean
        :param is_locked: boolean
        :param is_incremental: boolean
        :param scan_risk: int
        :param scan_risk_severity: int
        :param engine_server: CxEngineServer
        :param finished_scan_status: CxFinishedStatus
        :param partial_scan_reasons: list of str
        """
        self.id = id
        self.project = project
        self.status = status
        self.scan_type = scan_type
        self.comment = comment
        self.date_and_time = date_and_time
        self.results_statistics = results_statistics
        self.scan_state = scan_state
        self.owner = owner
        self.origin = origin
        self.initiator_name = initiator_name
        self.owning_team_id = owning_team_id
        self.is_public = is_public
        self.is_locked = is_locked
        self.is_incremental = is_incremental
        self.scan_risk = scan_risk
        self.scan_risk_severity = scan_risk_severity
        self.engine_server = engine_server
        self.finished_scan_status = finished_scan_status
        self.partial_scan_reasons = partial_scan_reasons
