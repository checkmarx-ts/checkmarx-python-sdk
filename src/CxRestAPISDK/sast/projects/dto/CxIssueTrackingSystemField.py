# encoding: utf-8


class CxIssueTrackingSystemField(object):
    """
    field
    """
    def __init__(self, id, name, multiple, required, supported, allowed_values):
        """

        :param id:
        :param name:
        :param multiple:
        :param required:
        :param supported:
        :param allowed_values: list of CxIssueTrackingSystemFieldAllowedValue
        """
        self.id = id
        self.name = name
        self.multiple = multiple
        self.required = required
        self.supported = supported
        self.allowed_values = allowed_values
