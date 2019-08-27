# encoding: utf-8


class CxDateAndTime(object):
    """
    scan date and time
    """
    def __init__(self, started_on=None, finished_on=None, engine_started_on=None, engine_finished_on=None):
        """

        Args:
            started_on (str):
            finished_on (str):
            engine_started_on (str):
            engine_finished_on (str):
        """
        self.started_on = started_on
        self.finished_on = finished_on
        self.engine_started_on = engine_started_on
        self.engine_finished_on = engine_finished_on

    def __str__(self):
        return "CxDateAndTime(started_on={}, finished_on={}, engine_started_on={}, engine_finished_on={})".format(
            self.started_on, self.finished_on, self.engine_started_on, self.engine_finished_on
        )
