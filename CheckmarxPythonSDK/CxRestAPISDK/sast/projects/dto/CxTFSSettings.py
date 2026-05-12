# encoding: utf-8
from .CxLink import CxLink
from .CxURI import CxURI


class CxTFSSettings(object):
    """
    TFS settings
    """

    def __init__(self, uri, paths, link=None, credentials=None):
        self.uri = uri
        self.paths = paths
        self.link = link
        self.credentials = credentials

    @classmethod
    def from_dict(cls, item: dict) -> "CxTFSSettings":
        return cls(
            uri=CxURI.from_dict(item.get("uri") or {}),
            paths=item.get("paths"),
            link=CxLink.from_dict(item.get("link") or {}),
        )

    def to_dict(self):
        return {
            "credentials": {
                "userName": self.credentials.username,
                "password": self.credentials.password,
            },
            "uri": {"absoluteUrl": self.uri.absolute_url, "port": self.uri.port},
            "paths": self.paths,
        }

    def __str__(self):
        return "CxTFSSettings(uri={}, paths={}, link={}, credentials={})".format(
            self.uri, self.paths, self.link, self.credentials
        )
