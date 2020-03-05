# encoding: utf-8


class CxOsaLocation(object):
    """
    location
    """
    def __init__(self, path, match_type):
        """

        Args:
            path (str):
            match_type (:obj:`CxOsaMatchType`):
        """
        self.path = path
        self.match_type = match_type

    def __str__(self):
        return """CxOsaLocation(path={}, match_type={})""".format(
            self.path, self.match_type
        )
