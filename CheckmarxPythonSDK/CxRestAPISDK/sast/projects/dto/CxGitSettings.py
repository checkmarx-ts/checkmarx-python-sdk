# encoding: utf-8
from .CxLink import CxLink


class CxGitSettings(object):
    """
    git settings
    """

    def __init__(self, url, branch, use_ssh=False, link=None, private_key=None):
        self.url = url
        self.branch = branch
        self.use_ssh = use_ssh
        self.link = link
        self.private_key = private_key

    @classmethod
    def from_dict(cls, item: dict) -> "CxGitSettings":
        return cls(
            url=item.get("url"),
            branch=item.get("branch"),
            use_ssh=item.get("useSsh", False),
            link=CxLink.from_dict(item.get("link") or {}),
            private_key=item.get("privateKey"),
        )

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
