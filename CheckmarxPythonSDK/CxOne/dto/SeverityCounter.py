class SeverityCounter(object):

    def __init__(self, severity, counter):
        """

        Args:
            severity (str): The severity level of the vulnerability.
            counter (int): The number of vulnerabilities found at this severity level.
        """
        self.severity = severity
        self.counter = counter

    def __str__(self):
        return """SeverityCounter(severity={}, counter={})""".format(
            self.severity, self.counter
        )
