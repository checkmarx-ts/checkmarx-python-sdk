# encoding: utf-8

import json


class CxSharedRemoteSourceSettingsRequest(object):
    """
    the request body
    """
    def __init__(self, paths, credentials):
        """

        :param paths: list of paths
        :param credentials: CxCredential
        """
        self.paths = paths
        self.credentials = credentials

    def get_post_data(self):
        return json.dumps(
            {
                "paths": self.paths,
                "credentials": {
                    "userName": self.credentials.username,
                    "password": self.credentials.password
                }
            }
        )
