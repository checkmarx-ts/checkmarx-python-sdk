# encoding: utf-8
from .CxLink import CxLink
from .CxURI import CxURI


class CxPerforceSettings(object):
    """
    perforce settings
    """

    def __init__(self, uri, paths, browse_mode="Depot", link=None, credentials=None):
        self.uri = uri
        self.paths = paths
        self.browse_mode = browse_mode
        self.link = link
        self.credentials = credentials

    @classmethod
    def from_dict(cls, item: dict) -> "CxPerforceSettings":
        return cls(
            uri=CxURI.from_dict(item.get("uri") or {}),
            paths=item.get("paths"),
            browse_mode=item.get("browseMode", "Depot"),
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
            "browseMode": self.browse_mode,
        }

    def __str__(self):
        return "CxPerforceSettings(uri={}, paths={}, browse_mode={}, link={}, credentials={})".format(
            self.uri, self.paths, self.browse_mode, self.link, self.credentials
        )
