# encoding: utf-8


class CxIssueTrackingSystemType(object):
    """
    one of issue types
    """
    def __init__(self, id, name, sub_task, fields):
        """

        :param id: str
        :param name: str
        :param sub_task: boolean
        :param fields: list of CxIssueTrackingSystemField
        """
        self.id = id
        self.name = name
        self.sub_task = sub_task
        self.fields = fields
