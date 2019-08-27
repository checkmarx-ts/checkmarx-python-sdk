# encoding: utf-8


class CxCreateScanSettingsResponse(object):
    """
    create scan settings response
    """

    def __init__(self, scan_setting_response_id=None, link=None):
        """

        Args:
            scan_setting_response_id (int):
            link (:obj:`CxLink`):
        """
        self.id = scan_setting_response_id
        self.link = link

    def __str__(self):
        return "CxCreateScanSettingsResponse(scan_setting_response_id={}, link={})".format(
            self.id, self.link
        )
