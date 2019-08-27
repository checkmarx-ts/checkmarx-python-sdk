# encoding: utf-8


class CxURI(object):
    """
    the URI settings
    """

    def __init__(self, absolute_url, port):
        """

        Args:
            absolute_url (str):
            port (int):
        """
        self.absolute_url = absolute_url
        self.port = port

    def __str__(self):
        return "CxURI(absolute_url={}, port={})".format(
            self.absolute_url, self.port
        )
