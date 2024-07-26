class TotalCounters(object):

    def __init__(self, severity_counters):
        """

        Args:
            severity_counters (list of SeverityCounter):
        """
        self.severity_counters = severity_counters

    def __str__(self):
        return """TotalCounters(severity_counters={})""".format(
            self.severity_counters
        )
