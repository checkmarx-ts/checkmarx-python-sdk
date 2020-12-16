# encoding: utf-8

import json


class CxRegisterEngineRequestBody(object):
    """
    the request body to register engine
    """

    def __init__(self, name, uri, min_loc, max_loc, is_blocked, max_scans=None):
        """

        Args:
            name (str):
            uri (str):
            min_loc (int):
            max_loc (int):
            is_blocked (boolean):
        """
        self.name = name
        self.uri = uri
        self.min_loc = min_loc
        self.max_loc = max_loc
        self.is_blocked = is_blocked
        self.max_scans = max_scans

    def get_post_data(self):
        d = {
            "name": self.name,
            "uri": self.uri,
            "minLoc": self.min_loc,
            "maxLoc": self.max_loc,
            "isBlocked": self.is_blocked
        }
        if self.max_scans:
            d.update({"maxScans": self.max_scans})
        return json.dumps(d)

    def __str__(self):
        return "CxRegisterEngineRequestBody(name={}, uri={}, min_loc={}, max_loc={}, is_blocked={})".format(
            self.name, self.uri, self.min_loc, self.max_loc, self.is_blocked
        )
