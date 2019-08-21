# encoding: utf-8


class CxDateAndTime(object):
    """
    scan date and time
    """
    def __init__(self, started_on=None, finished_on=None, engine_started_on=None, engine_finished_on=None):
        """

        :param started_on: str
        :param finished_on: str
        :param engine_started_on: str
        :param engine_finished_on:
        """
        self.started_on = started_on
        self.finished_on = finished_on
        self.engine_started_on = engine_started_on
        self.engine_finished_on = engine_finished_on
