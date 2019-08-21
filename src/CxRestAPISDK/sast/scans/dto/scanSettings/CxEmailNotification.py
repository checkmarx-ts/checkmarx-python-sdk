# encoding: utf-8


class CxEmailNotification(object):
    """
    email notification
    """
    def __init__(self, failed_scan=None, before_scan=None, after_scan=None):
        """

        :param failed_scan: list
        :param before_scan: list
        :param after_scan: list
        """
        self.failed_scan = failed_scan
        self.before_scan = before_scan
        self.after_scan = after_scan
