# encoding: utf-8


class CxCustomTask(object):
    """
    custom tasks
    """

    def __init__(self, id, name, type, data, link):
        """

        :param id: int
        :param name: str
        :param type: str
        :param data: str
        :param link: CxLink
        """
        self.id = id
        self.name = name
        self.type = type
        self.data = data
        self.link = link

