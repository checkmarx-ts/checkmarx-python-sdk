# encoding: utf-8


class CxCustomRemoteSourceSettings(object):
    """
    source pulling
    """

    def __init__(self, path, pulling_command_id, link):
        """

        :param path:
        :param pulling_command_id:
        :param link: CxLink.CxLink
        """
        self.path = path
        self.pulling_command_id = pulling_command_id
        self.link = link
