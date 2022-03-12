class ReportStatusDTO(object):
    def __init__(self, report_id, report_status, creation_date, message):
        """

        Args:
            report_id (int):
            report_status (str, optional):
            creation_date (str):
            message (str, optional):
        """
        self.reportId = report_id
        self.reportStatus = report_status
        self.creationDate =creation_date
        self.message = message

    def __str__(self):
        return """ReportStatusDTO(reportId={}, reportStatus={}, creationDate={}, message={})""".format(
            self.reportId, self.reportStatus, self.creationDate, self.message
        )
