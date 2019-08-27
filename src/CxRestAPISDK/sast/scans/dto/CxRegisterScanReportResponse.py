# encoding: utf-8


class CxRegisterScanReportResponse(object):
    """
    the response of register scan report
    """

    class Links(object):
        def __init__(self, report, status):
            """

            Args:
                report (:obj:`CxLink`):
                status (:obj:`CxLink`):
            """
            self.report = report
            self.status = status

    def __init__(self, report_id, links):
        """

        Args:
            report_id (int):
            links (:obj:`CxRegisterScanReportResponse.Links`):
        """
        self.report_id = report_id
        self.links = links

    def __str__(self):
        return "CxRegisterScanReportResponse(report_id={}, links={})".format(
            self.report_id, self.links
        )
