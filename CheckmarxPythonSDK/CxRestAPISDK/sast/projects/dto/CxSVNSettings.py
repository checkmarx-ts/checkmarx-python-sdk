# encoding: utf-8
from .CxLink import CxLink
from .CxURI import CxURI


class CxSVNSettings(object):
    """
    svn settings
    """

    def __init__(
        self, uri, paths, use_ssh=None, link=None, credentials=None, private_key=None
    ):
        self.uri = uri
        self.paths = paths
        self.use_ssh = use_ssh
        self.link = link
        self.credentials = credentials
        self.private_key = private_key

    @classmethod
    def from_dict(cls, item: dict) -> "CxSVNSettings":
        return cls(
            uri=CxURI.from_dict(item.get("uri") or {}),
            paths=item.get("paths", []),
            use_ssh=item.get("useSsh"),
            link=CxLink.from_dict(item.get("link") or {}),
        )

    def to_dict(self):
        data = {
            "uri": {"absoluteUrl": self.uri.absolute_url, "port": self.uri.port},
            "paths": self.paths,
            "credentials": {
                "userName": self.credentials.username,
                "password": self.credentials.password,
            },
        }
        if self.private_key:
            data.update({"privateKey": self.private_key})
        return data

    def __str__(self):
        return "CxSVNSettings(uri={}, paths={}, use_ssh={}, link={}, credentials={}, private_key={})".format(
            self.uri,
            self.paths,
            self.use_ssh,
            self.link,
            self.credentials,
            self.private_key,
        )
