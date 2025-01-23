# encoding: utf-8
import json


class CxCustomRemoteSourceSettings(object):
    """
    source pulling
    """

    def __init__(self, path, pulling_command_id, link=None, credentials=None):
        """

        Args:
            path (str):
            pulling_command_id (int):
            link (:obj:`CxLink`):
            credentials (CxCredential):
        """
        self.path = path
        self.pulling_command_id = pulling_command_id
        self.link = link
        self.credentials = credentials

    def to_dict(self):
        return {
                "path": self.path,
                "preScanCommandId": self.pulling_command_id,
                "credentials": {
                    "userName": self.credentials.username,
                    "password": self.credentials.password
                }
            }

    def __str__(self):
        return "CxCustomRemoteSourceSettings(path={}, pulling_command_id={}, link={}, credentials={})".format(
            self.path, self.pulling_command_id, self.link, self.credentials
        )
