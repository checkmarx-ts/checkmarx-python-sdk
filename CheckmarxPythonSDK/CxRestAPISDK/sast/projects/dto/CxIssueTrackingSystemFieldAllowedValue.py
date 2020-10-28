# encoding: utf-8


class CxIssueTrackingSystemFieldAllowedValue(object):
    """
    allowed value
    """

    def __init__(self, allowed_value_id, name):
        """

        Args:
            allowed_value_id (str):
            name (str):
        """
        self.id = allowed_value_id
        self.name = name

    def __str__(self):
        return "CxIssueTrackingSystemFieldAllowedValue(id={}, name={})".format(
            self.id, self.name
        )
