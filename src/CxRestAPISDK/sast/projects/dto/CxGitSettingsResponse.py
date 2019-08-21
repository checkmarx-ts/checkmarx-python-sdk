# encoding: utf-8


class CxGitSettingsResponse(object):
    """
    git settings
    """

    def __init__(self, url, branch, use_ssh, link):
        """

        :param url: url
        :param branch: url
        :param use_ssh: boolean
        :param link: CxLink
        """
        self.url = url
        self.branch = branch
        self.use_ssh = use_ssh
        self.link = link
