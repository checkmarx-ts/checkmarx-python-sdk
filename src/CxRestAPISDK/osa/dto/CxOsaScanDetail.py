# encoding: utf-8


class CxOsaScanDetail(object):
    """
    osa scan detail
    """
    def __init__(self, findings_status, scan_detail_id, start_analyze_time, end_analyze_time, origin,
                 source_code_origin, state, shared_source_location_paths):
        """

        Args:
            findings_status (str):
            scan_detail_id (str):
            start_analyze_time (str):
            end_analyze_time (str):
            origin (str):
            source_code_origin (str):
            state (:obj:`CxOsaState`):
            shared_source_location_paths(:obj:`list` of :obj:`str`):
        """
        self.findings_status = findings_status
        self.id = scan_detail_id
        self.start_analyze_time = start_analyze_time
        self.end_analyze_time = end_analyze_time
        self.origin = origin
        self.source_code_origin = source_code_origin
        self.state = state
        self.shared_source_location_paths = shared_source_location_paths

    def __str__(self):
        return """CxOsaScanDetail(findings_status={}, id={}, start_analyze_time={}, end_analyze_time={}, 
                origin={}, source_code_origin={}, state={}, shared_source_location_paths={})""".format(
            self.findings_status, self.id, self.start_analyze_time, self.end_analyze_time,
            self.origin, self.source_code_origin, self.state, self.shared_source_location_paths
        )
