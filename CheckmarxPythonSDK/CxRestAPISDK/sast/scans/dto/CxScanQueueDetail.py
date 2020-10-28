# encoding: utf-8


class CxScanQueueDetail(object):
    """
    scan queue detail
    """
    def __init__(self, scan_queue_detail_id=None, stage=None, stage_details=None, step_details=None, project=None,
                 engine=None, languages=None, team_id=None, date_created=None, queued_on=None, engine_started_on=None,
                 completed_on=None, loc=None, is_incremental=None, is_public=None, origin=None, queue_position=None,
                 total_percent=None, stage_percent=None, initiator=None):
        """

        Args:
            scan_queue_detail_id (int):
            stage (:obj:`CxScanStage`):
            stage_details (str):
            step_details (str):
            project (:obj:`CxProject`):
            engine (:obj:`CxEngineServer`):
            languages (:obj:`list` of :obj:`CxLanguage`):
            team_id (str):
            date_created (str):
            queued_on (str):
            engine_started_on (str):
            completed_on (str):
            loc (int):
            is_incremental (boolean):
            is_public (boolean):
            origin (str):
            queue_position (int):
            total_percent (int):
            stage_percent (int):
            initiator (str):
        """
        self.id = scan_queue_detail_id
        self.stage = stage
        self.stage_details = stage_details
        self.step_details = step_details
        self.project = project
        self.engine = engine
        self.languages = languages
        self.team_id = team_id
        self.date_created = date_created
        self.queued_on = queued_on
        self.engine_started_on = engine_started_on
        self.completed_on = completed_on
        self.loc = loc
        self.is_incremental = is_incremental
        self.is_public = is_public
        self.origin = origin
        self.queue_position = queue_position
        self.total_percent = total_percent
        self.stage_percent = stage_percent
        self.initiator = initiator

    def __str__(self):
        return """CxScanQueueDetail(id={}, stage={}, stage_details={}, step_details={}, project={}, engine={},
                 languages={}, team_id={}, date_created={}, queued_on={}, engine_started_on={},
                 completed_on={}, loc={}, is_incremental={}, is_public={}, origin={}, queue_position={},
                 total_percent={}, stage_percent={}, initiator={})""".format(
            self.id, self.stage, self.stage_details, self.step_details, self.project, self.engine,
            self.languages, self.team_id, self.date_created, self.queued_on, self.engine_started_on,
            self.completed_on, self.loc, self.is_incremental, self.is_public, self.origin, self.queue_position,
            self.total_percent, self.stage_percent, self.initiator
        )
