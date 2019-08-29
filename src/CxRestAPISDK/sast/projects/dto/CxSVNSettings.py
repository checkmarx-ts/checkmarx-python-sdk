# encoding: utf-8

import json


class CxSVNSettings(object):
    """
    svn settings
    """

    def __init__(self, uri, paths, use_ssh=None, link=None, credentials=None, private_key=None):
        """

        Args:
            uri (:obj:`CxURI`):
            paths (:obj:`list` of :obj:`str`):
            use_ssh (boolean):
            link (:obj:`CxLink`):
            credentials (:obj:`CxCredential`):
            private_key (str):
        """
        self.uri = uri
        self.paths = paths
        self.use_ssh = use_ssh
        self.link = link
        self.credentials = credentials
        self.private_key = private_key

    def get_post_data(self):

        target_dict = {
            "uri": {
                "absoluteUrl": self.uri.absolute_url,
                "port": self.uri.port
            },
            "paths": self.paths,
            "credentials": {
                "userName": self.credentials.username,
                "password": self.credentials.password
            }
        }

        if self.private_key:
            target_dict.update({"privateKey": self.private_key})

        return json.dumps(target_dict)

    def __str__(self):
        return "CxSVNSettings(uri={}, paths={}, use_ssh={}, link={}, credentials={}, private_key={})".format(
            self.uri, self.paths, self.use_ssh, self.link, self.credentials, self.private_key
        )
