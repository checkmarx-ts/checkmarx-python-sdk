# encoding: utf-8


class CxCreateNewScanResponse(object):
    """
    create new scan response
    """

    def __init__(self, scan_id, link):
        """

        Args:
            scan_id (int):
            link (:obj:`CxLink`):
        """
        self.id = scan_id
        self.link = link

    def __str__(self):
        return "CxCreateNewScanResponse(id={}, link={})".format(
            self.id, self.link
        )
