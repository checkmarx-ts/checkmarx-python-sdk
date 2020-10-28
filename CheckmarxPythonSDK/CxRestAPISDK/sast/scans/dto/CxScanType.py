# encoding: utf-8


class CxScanType(object):
    """
    scan type
    """

    def __init__(self, scan_type_id, value):
        """

        Args:
            scan_type_id (int):
            value (str):
        """
        self.id = scan_type_id
        self.value = value

    def __str__(self):
        return "CxScanType(id={}, value={})".format(
            self.id, self.value
        )
