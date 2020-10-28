# encoding: utf-8


class CxIssueTrackingSystemJiraField(object):
    """
    jira field
    """
    def __init__(self, field_id, values):
        """

        Args:
            field_id (str):
            values (:obj:`list` of :obj:`str`):
        """
        self.id = field_id
        self.values = values

    def __str__(self):
        return "CxIssueTrackingSystemJiraField(id={}, values={})".format(
            self.id, self.values
        )
