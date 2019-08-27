# encoding: utf-8

import json


class CxGitSettings(object):
    """
    git settings
    """

    def __init__(self, url, branch, use_ssh=False, link=None, private_key=None):
        """

        Args:
            url (str):
            branch (str):
            use_ssh (bool):
            link (:obj:`CxLink`):
        """
        self.url = url
        self.branch = branch
        self.use_ssh = use_ssh
        self.link = link
        self.private_key = private_key

    def get_post_data(self):
        return json.dumps(
            {
                "url": self.url,
                "branch": self.branch,
                "privateKey": self.private_key
            }
        )

    def __str__(self):
        return "CxGitSettings(url={}, branch={}, use_ssh={}, link={})".format(
            self.url, self.branch, self.use_ssh, self.link
        )
