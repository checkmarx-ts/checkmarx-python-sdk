# encoding: utf-8

import json


class CxRegisterEngineRequestBody(object):
    """
    the request body to register engine
    """

    def __init__(self, name, uri, min_loc, max_loc, is_blocked):
        """

        :param name: str
        :param uri: str
        :param min_loc: int
        :param max_loc: int
        :param is_blocked: boolean
        """
        self.name = name
        self.uri = uri
        self.min_loc = min_loc
        self.max_loc = max_loc
        self.is_blocked = is_blocked

    def get_post_data(self):
        return json.dumps(
            {
                "name": self.name,
                "uri": self.uri,
                "minLoc": self.min_loc,
                "maxLoc": self.max_loc,
                "isBlocked": self.is_blocked
            }
        )
