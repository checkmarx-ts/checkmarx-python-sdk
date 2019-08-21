# encoding: utf-8


class CxPolicyFindingResponse(object):
    """
    policy finding response
    """
    def __init__(self, id, link):
        """

        :param id: int
        :param link:  CxLink.CxLink
        """
        self.id = id
        self.link = link
