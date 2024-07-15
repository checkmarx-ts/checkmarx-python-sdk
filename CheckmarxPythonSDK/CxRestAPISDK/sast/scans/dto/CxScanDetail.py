# encoding: utf-8


class CxScanDetail(object):
    """

    """

    def __init__(self, scan_id=None, project=None, status=None, scan_type=None, comment=None, date_and_time=None,
                 results_statistics=None, scan_state=None, owner=None, origin=None, origin_url=None,
                 initiator_name=None,
                 owning_team_id=None, is_public=None, is_locked=None, is_incremental=None, scan_risk=None,
                 scan_risk_severity=None, engine_server=None, finished_scan_status=None, partial_scan_reasons=None,
                 custom_fields=None):
        """

        Args:
            scan_id (int):
            project (:obj:`CxProject`):
            status (:obj:`CxStatus`):
            scan_type (:obj:`CxScanType`):
            comment (str):
            date_and_time (:obj:`CxDateAndTime`):
            results_statistics (:obj:`CxResultStatistics`):
            scan_state (:obj:`CxScanState`):
            owner (str):
            origin (str):
            origin_url (str):
            initiator_name (str):
            owning_team_id (int):
            is_public (boolean):
            is_locked (boolean):
            is_incremental (boolean):
            scan_risk (int):
            scan_risk_severity (int):
            engine_server (:obj:`CxEngineServer`):
            finished_scan_status (:obj:`CxFinishedStatus`):
            partial_scan_reasons (:obj:`list` of :obj:`str`):
        """
        self.id = scan_id
        self.project = project
        self.status = status
        self.scan_type = scan_type
        self.comment = comment
        self.date_and_time = date_and_time
        self.results_statistics = results_statistics
        self.scan_state = scan_state
        self.owner = owner
        self.origin = origin
        self.origin_url = origin_url
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
        self.custom_fields = custom_fields

    def __str__(self):
        return """CxScan(id={}, project={}, status={}, scan_type={}, comment={}, date_and_time={},
                 results_statistics={}, scan_state={}, owner={}, origin={}, origin_url={}, initiator_name={},
                 owning_team_id={}, is_public={}, is_locked={}, is_incremental={}, scan_risk={},
                 scan_risk_severity={}, engine_server={}, finished_scan_status={}, partial_scan_reasons={},
                 custom_fields={})""".format(
            self.id, self.project, self.status, self.scan_type, self.comment, self.date_and_time,
            self.results_statistics, self.scan_state, self.owner, self.origin, self.origin_url, self.initiator_name,
            self.owning_team_id, self.is_public, self.is_locked, self.is_incremental, self.scan_risk,
            self.scan_risk_severity, self.engine_server, self.finished_scan_status, self.partial_scan_reasons,
            self.custom_fields
        )
