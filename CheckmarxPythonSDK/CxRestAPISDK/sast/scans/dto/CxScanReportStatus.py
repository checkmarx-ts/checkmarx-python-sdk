# encoding: utf-8


class CxScanReportStatus(object):
    """
    scan report status
    """
    class Status(object):
        def __init__(self, status_id, value):
            """

            Args:
                status_id (int):
                value (str):
            """
            self.id = status_id
            self.value = value

    def __init__(self, link, content_type, status):
        """

        Args:
            link (:obj:`CxLink`):
            content_type (str):
            status (:obj:`CxScanReportStatus.Status`):
        """
        self.link = link
        self.content_type = content_type
        self.status = status

    def __str__(self):
        return "CxScanReportStatus(link={}, content_type={}, status={})".format(
            self.link, self.content_type, self.status
        )
