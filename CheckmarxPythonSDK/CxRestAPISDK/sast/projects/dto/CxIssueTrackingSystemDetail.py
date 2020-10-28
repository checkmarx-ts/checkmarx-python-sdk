# encoding: utf-8


class CxIssueTrackingSystemDetail(object):

    """
    issue tracking system
    """
    def __init__(self, tracking_system_detail_id, name, issue_types=None):
        """

        Args:
            tracking_system_detail_id (int):
            name (str):
            issue_types (:obj:`list` of :obj:`CxIssueTrackingSystemType`):
        """
        self.id = tracking_system_detail_id
        self.name = name
        self.issue_types = issue_types

    def __str__(self):
        return "CxIssueTrackingSystemDetail(id={}, name={}, issue_types={})".format(
            self.id, self.name, self.issue_types
        )
