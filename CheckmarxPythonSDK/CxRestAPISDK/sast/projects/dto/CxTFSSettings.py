# encoding: utf-8
import json


class CxTFSSettings(object):
    """
    TFS settings
    """
    def __init__(self, uri, paths, link=None, credentials=None):
        """

        Args:
            uri (:obj:`CxURI`):
            paths (:obj:`list` of :obj:`str`):
            link (:obj:`CxLink`):
            credentials (:obj:`CxCredential`):
        """
        self.uri = uri
        self.paths = paths
        self.link = link
        self.credentials = credentials

    def to_dict(self):
        return {
                "credentials": {
                    "userName": self.credentials.username,
                    "password": self.credentials.password
                },
                "uri": {
                    "absoluteUrl": self.uri.absolute_url,
                    "port": self.uri.port
                },
                "paths": self.paths,
            }

    def __str__(self):
        return "CxTFSSettings(uri={}, paths={}, link={}, credentials={})".format(
            self.uri, self.paths, self.link, self.credentials
        )
