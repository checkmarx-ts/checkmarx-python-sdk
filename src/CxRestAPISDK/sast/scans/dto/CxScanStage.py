# encoding: utf-8


class CxScanStage(object):
    """
    scan stage
    """

    def __init__(self, scan_stage_id, value):
        """

        Args:
            scan_stage_id (int):
            value (str):
        """
        self.id = scan_stage_id
        self.value = value

    def __str__(self):
        return "CxScanStage(id={}, value={})".format(
            self.id, self.value
        )
