# encoding: utf-8


class CxScanReportStatus(object):
    """
    scan report status
    """
    class Status(object):
        def __init__(self, id, value):
            """

            :param id: int
            :param value: str
            """
            self.id = id
            self.value = value

    def __init__(self, link, content_type, status):
        """

        :param link: CxLink
        :param content_type:
        :param status:
        """
        self.link = link
        self.content_type = content_type
        self.status = status
