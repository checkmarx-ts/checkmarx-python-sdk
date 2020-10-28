# encoding: utf-8


class CxStatus(object):
    """
    scan status
    """

    def __init__(self, status_id=None, name=None, details=None):
        """

        Args:
            status_id (int):
            name (str):
            details (:obj:`CxStatusDetail`):
        """
        self.id = status_id
        self.name = name
        self.details = details

    def __str__(self):
        return "CxStatus(id={}, name={}, details={})".format(
            self.id, self.name, self.details
        )
