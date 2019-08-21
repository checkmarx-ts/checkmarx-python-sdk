# encoding: utf-8


class CxIssueTrackingSystem(object):
    """
    issue tracking system
    """
    def __init__(self, id, name, type, url):
        """

        :param id: int
        :param name: str
        :param type: str
            example: jira
        :param url: str
        """
        self.id = id
        self.name = name
        self.type = type
        self.url = url
