# encoding: utf-8

import json


class CxSharedRemoteSourceSettingsRequest(object):
    """
    the request body
    """
    def __init__(self, paths, credentials):
        """

        Args:
            paths (:obj:`list` of :obj:`str`):
            credentials (:obj:`CxCredential`):
        """
        self.paths = paths
        self.credentials = credentials

    def to_dict(self):
        return {
                "paths": self.paths,
                "credentials": {
                    "userName": self.credentials.username,
                    "password": self.credentials.password
                }
            }

    def __str__(self):
        return "CxSharedRemoteSourceSettingsRequest(paths={}, credentials={})".format(
            self.paths, self.credentials
        )
