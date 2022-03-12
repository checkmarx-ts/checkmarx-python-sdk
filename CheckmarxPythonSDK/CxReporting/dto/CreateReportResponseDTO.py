class CreateReportResponseDTO(object):
    def __init__(self, report_id):
        """

        Args:
            report_id (str):
        """
        self.reportId = report_id

    def __str__(self):
        return """CreateReportResponseDTO(reportId={})""".format(
            self.reportId
        )
