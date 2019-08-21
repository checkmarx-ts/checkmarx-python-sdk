# encoding: utf-8


class CxPreset(object):
    """
    the queries set
    """

    def __init__(self, id, name, owner_name, link, query_ids=None):
        """

        :param id: int
        :param name: str
        :param owner_name: str
        :param link: CxLink CxLink
        :param query_ids: list of int
        """
        self.id = id
        self.name = name
        self.owner_name = owner_name
        self.link = link
        self.query_ids = query_ids
