# encoding: utf-8


class CxIssueTrackingSystem(object):
    """
    issue tracking system
    """
    def __init__(self, tracking_system_id, name, tracking_system_type, url):
        """

        Args:
            tracking_system_id (int):
            name (str):
            tracking_system_type (str):  eg, "jira"
            url (str):
        """
        self.id = tracking_system_id
        self.name = name
        self.type = tracking_system_type
        self.url = url

    def __str__(self):
        return "CxIssueTrackingSystem(id={}, name={}, tracking_system_type={}, url={})".format(
            self.id, self.name, self.type, self.url
        )
