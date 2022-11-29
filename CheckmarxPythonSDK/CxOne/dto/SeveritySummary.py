class SeveritySummary(object):
    def __init__(self, severity, count):
        """

        Args:
            severity (str): Severity enum of a result. Enum: [ HIGH, MEDIUM, LOW, INFO ]
            count (int):
        """
        self.severity = severity
        self.count = count

    def __str__(self):
        return """SeveritySummary(severity={}, count={})""".format(
            self.severity, self.count
        )
