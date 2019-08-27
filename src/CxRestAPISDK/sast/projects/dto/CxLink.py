# encoding: utf-8


class CxLink(object):
    """
    the link information of a project
    """

    def __init__(self, rel, uri):
        """

        Args:
            rel (str):
            uri (str):
        """
        self.rel = rel
        self.uri = uri

    def __str__(self):
        return "CxLink(rel={}, uri={})".format(
            self.rel, self.uri
        )
