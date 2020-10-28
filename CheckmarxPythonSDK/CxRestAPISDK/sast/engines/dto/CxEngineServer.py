# encoding: utf-8


class CxEngineServer(object):
    """
    engine server
    """

    def __init__(self, engine_server_id=None, name=None, uri=None, min_loc=None, max_loc=None, max_scans=None,
                 cx_version=None, status=None, link=None):
        """

        Args:
            engine_server_id (int):
            name (str):
            uri (str):
            min_loc (int):
            max_loc (int):
            max_scans (int):
            cx_version (str):
            status (:obj:`CxEngineServerStatus`):
            link (:obj:`CxLink`):
        """
        self.id = engine_server_id
        self.name = name
        self.uri = uri
        self.min_loc = min_loc
        self.max_loc = max_loc
        self.max_scans = max_scans
        self.cx_version = cx_version
        self.status = status
        self.link = link

    def __str__(self):
        return """CxEngineServer(id={}, name={}, uri={}, min_loc={}, max_loc={}, max_scans={}, 
                 cx_version={}, status={}, link={})""".format(
            self.id, self.name, self.uri, self.min_loc, self.max_loc, self.max_scans,
            self.cx_version, self.status, self.link
        )
