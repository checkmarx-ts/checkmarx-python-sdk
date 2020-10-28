# encoding: utf-8


class CxFinishedScanStatus(object):
    """
    finished scan status
    """
    def __init__(self, scan_status_id=None, value=None):
        """

        Args:
            scan_status_id (int):
            value (str):
        """
        self.id = scan_status_id
        self.value = value

    def __str__(self):
        return "CxFinishedScanStatus(id={}, value={}))".format(
            self.id, self.value
        )
