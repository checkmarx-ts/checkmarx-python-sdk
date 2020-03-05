# encoding: utf-8


class CxStatusDetail(object):
    """
    scan status detail
    """

    def __init__(self, stage, step):
        """

        Args:
            stage (str):
            step (str):
        """
        self.stage = stage
        self.step = step

    def __str__(self):
        return "CxStatusDetail(stage={}, step={})".format(
            self.stage, self.step
        )
