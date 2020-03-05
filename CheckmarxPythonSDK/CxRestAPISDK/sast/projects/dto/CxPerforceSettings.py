# encoding: utf-8
import json


class CxPerforceSettings(object):
    """
    perforce settings
    """

    def __init__(self, uri, paths, browse_mode="Depot", link=None, credentials=None):
        """

        Args:
            uri (:obj:`CxURI`):
            paths (:obj:`list` of :obj:`str`):
            browse_mode (str): "Depot"
            link (:obj:`CxLink`):
        """
        self.uri = uri
        self.paths = paths
        self.browse_mode = browse_mode
        self.link = link
        self.credentials = credentials

    def get_post_data(self):
        return json.dumps(
            {
                "credentials": {
                    "userName": self.credentials.username,
                    "password": self.credentials.password,
                },
                "uri": {
                    "absoluteUrl": self.uri.absolute_url,
                    "port": self.uri.port
                },
                "paths": self.paths,
                "browseMode": self.browse_mode
            }
        )

    def __str__(self):
        return "CxPerforceSettings(uri={}, paths={}, browse_mode={}, link={}, credentials={})".format(
            self.uri, self.paths, self.browse_mode, self.link, self.credentials
        )
