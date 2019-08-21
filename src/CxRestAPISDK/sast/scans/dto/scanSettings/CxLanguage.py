# encoding: utf-8


class CxLanguage(object):
    """
    the languages that Checkmarx supported
    """
    def __init__(self, id, name):
        """

        :param id: int
        :param name: str
        """
        self.id = id
        self.name = name
