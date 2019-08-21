# encoding: utf-8


class CxLink(object):
    """
    the link information of a project
    """

    def __init__(self, rel, uri):
        """

        :param rel: str
        :param uri: str
        """
        self.rel = rel
        self.uri = uri
