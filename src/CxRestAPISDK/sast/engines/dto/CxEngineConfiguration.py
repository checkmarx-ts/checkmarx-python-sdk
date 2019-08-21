# encoding: utf-8


class CxEngineConfiguration(object):
    """
    engine configuration
    """
    def __init__(self, id=None, link=None, name=None):
        """

        :param id: int
        :param link: CxLink.CxLink
        """
        self.id = id
        self.link = link
        self.name = name
