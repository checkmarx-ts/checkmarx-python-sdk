# encoding: utf-8

import json


class CxCustomRemoteSourceSettingsRequest(object):
    """
    used for set remote source setting for custom by project id
    """

    def __init__(self, path, pre_scan_command_id, credentials):
        """

        :param path:  str
        :param pre_scan_command_id:  int
        :param credentials: CxCredential
        """
        self.path = path
        self.pre_scan_command_id = pre_scan_command_id
        self.credentials = credentials

    def get_post_data(self):
        return json.dumps(
            {
                "path": self.path,
                "preScanCommandId": self.pre_scan_command_id,
                "credentials": {
                    "userName": self.credentials.username,
                    "password": self.credentials.password
                }
            }
        )
