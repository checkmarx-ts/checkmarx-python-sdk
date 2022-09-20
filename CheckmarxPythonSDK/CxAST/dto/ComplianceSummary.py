class ComplianceSummary(object):
    def __init__(self, compliance, count):
        """

        Args:
            compliance (str):
            count (int):
        """
        self.compliance = compliance
        self.count = count

    def __str__(self):
        return """ComplianceSummary(compliance={}, count={})""".format(
            self.compliance, self.count
        )
