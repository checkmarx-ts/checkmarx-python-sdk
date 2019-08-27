# encoding: utf-8


class CxOsaSeverity(object):
    """
    severity
    """
    def __init__(self, severity_id, name):
        """

        Args:
            severity_id (int):
            name  (str): eg. "High"
        """

        self.id = severity_id
        self.name = name

    def __str__(self):
        return """CxOsaSeverity(id={}, name={})""".format(
            self.id, self.name
        )
