# encoding: utf-8

import json


class CxGitSettingsPostRequest(object):
    """
    git setting request body
    """

    def __init__(self, url, branch, private_key):
        """

        :param url: str
        :param branch: str
        :param private_key: str
        """
        self.url = url
        self.branch = branch
        self.private_key = private_key

    def get_post_data(self):
        return json.dumps(
            {
                "url": self.url,
                "branch": self.branch,
                "privateKey": self.private_key
            }
        )
