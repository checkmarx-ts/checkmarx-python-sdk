# encoding: utf-8


class CxIssueTrackingSystemDetail(object):

    """
    issue tracking system
    """
    def __init__(self, id, name, issue_types=None):
        """

        :param id: int
        :param name: str
        :param issue_types: list of CxIssueTrackingSystemType
        """
        self.id = id
        self.name = name
        self.issue_types = issue_types
