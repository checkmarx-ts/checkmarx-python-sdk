# encoding: utf-8


class CxCreateNewScanResponse(object):
    """
    create new scan response
    """

    def __init__(self, scan_id, link):
        """

        :param scan_id: int
        :param link: CxLink.CxLink
        """
        self.id = scan_id
        self.link = link
