# encoding: utf-8


class CxIssueTrackingSystemType(object):
    """
    one of issue types
    """
    def __init__(self, issue_tracking_system_type_id, name, sub_task, fields):
        """

        Args:
            issue_tracking_system_type_id (str):
            name (str):
            sub_task (boolean):
            fields (:obj:`list` of :obj:`CxIssueTrackingSystemField`):
        """
        self.id = issue_tracking_system_type_id
        self.name = name
        self.sub_task = sub_task
        self.fields = fields

    def __str__(self):
        return "CxIssueTrackingSystemType(id={}, name={}, sub_task={}, fields={})".format(
            self.id, self.name, self.sub_task, self.fields
        )
