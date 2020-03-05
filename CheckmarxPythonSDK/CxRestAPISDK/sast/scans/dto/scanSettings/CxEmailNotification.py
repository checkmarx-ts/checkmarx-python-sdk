# encoding: utf-8


class CxEmailNotification(object):
    """
    email notification
    """
    def __init__(self, failed_scan=None, before_scan=None, after_scan=None):
        """

        Args:
            failed_scan (:obj:`list` of :obj:`str`):
            before_scan (:obj:`list` of :obj:`str`):
            after_scan (:obj:`list` of :obj:`str`):
        """
        self.failed_scan = failed_scan
        self.before_scan = before_scan
        self.after_scan = after_scan

    def __str__(self):
        return "CxEmailNotification(failed_scan={}, before_scan={}, after_scan={})".format(
            self.failed_scan, self.before_scan, self.after_scan
        )
