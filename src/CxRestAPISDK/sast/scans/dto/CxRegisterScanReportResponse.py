# encoding: utf-8


class CxRegisterScanReportResponse(object):
    """
    the response of register scan report
    """

    class Links(object):
        def __init__(self, report, status):
            """

            :param report: CxLink
            :param status: CxLink
            """
            self.report = report
            self.status = status

    def __init__(self, report_id, links):
        """

        :param report_id: int
        :param links: CxRegisterScanReportResponse.Links
        """
        self.report_id = report_id
        self.links = links
