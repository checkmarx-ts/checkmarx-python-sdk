# encoding: utf-8


class CxScanQueueDetail(object):
    """
    scan queue detail
    """
    def __init__(self, id=None, stage=None, stage_details=None, step_details=None, project=None, engine=None,
                 languages=None, team_id=None, date_created=None, queued_on=None, engine_started_on=None,
                 completed_on=None, loc=None, is_incremental=None, is_public=None, origin=None, queue_position=None,
                 total_percent=None, stage_percent=None, initiator=None):
        """

        :param id:
        :param stage:
        :param stage_details:
        :param step_details:
        :param project:
        :param engine:
        :param languages:
        :param team_id:
        :param date_created:
        :param queued_on:
        :param engine_started_on:
        :param completed_on:
        :param loc:
        :param is_incremental:
        :param is_public:
        :param origin:
        :param queue_position:
        :param total_percent:
        :param stage_percent:
        :param initiator:
        """
        self.id = id
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
