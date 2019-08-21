# encoding: utf-8


class CxEngineServer(object):
    """
    engine server
    """

    class Status(object):
        """
        engine status
        """
        def __init__(self, id=None, value=None):
            """

            :param id: int
            :param value: str
            """
            self.id = id
            self.value = value

    def __init__(self, id=None, name=None, uri=None, min_loc=None, max_loc=None, max_scans=None, cx_version=None,
                 status=None, link=None):
        """

        :param id: int
        :param name: str
        :param uri: str
        :param min_loc: int
        :param max_loc: int
        :param max_scans: int
        :param cx_version: str
        :param status: status
        :param link: CxProject.CxLink
        """
        self.id = id
        self.name = name
        self.uri = uri
        self.min_loc = min_loc
        self.max_loc = max_loc
        self.max_scans = max_scans
        self.cx_version = cx_version
        self.status = status
        self.link = link
