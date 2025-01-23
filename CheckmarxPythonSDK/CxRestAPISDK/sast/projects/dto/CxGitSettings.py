# encoding: utf-8
class CxGitSettings(object):
    """
    git settings
    """

    def __init__(self, url, branch, use_ssh=False, link=None, private_key=None):
        """

        Args:
            url (str):
            branch (str):
            use_ssh (boolean):
            link (:obj:`CxLink`):
        """
        self.url = url
        self.branch = branch
        self.use_ssh = use_ssh
        self.link = link
        self.private_key = private_key

    def to_dict(self):
        data = {
            "url": self.url,
            "branch": self.branch,
        }
        if self.private_key:
            data.update({"privateKey": self.private_key})
        return data

    def __str__(self):
        return "CxGitSettings(url={}, branch={}, use_ssh={}, link={})".format(
            self.url, self.branch, self.use_ssh, self.link
        )
