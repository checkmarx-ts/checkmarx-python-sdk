# encoding: utf-8

import json


class CxSVNSettings(object):
    """
    svn settings
    """

    class URI(object):
        """
        the URI of SVN settings
        """
        def __init__(self, absolute_url, port):
            self.absolute_url = absolute_url
            self.port = port

    def __init__(self, uri, paths, use_ssh=None, link=None, credentials=None, private_key=None):
        """

        :param uri: CxSVNSettingsResponse.URI
        :param paths: list of str
        :param use_ssh: boolean
        :param link: CxLink.CxLink
        :param credentials: CxCredential
        """
        self.uri = uri
        self.paths = paths
        self.use_ssh = use_ssh
        self.link = link
        self.credentials = credentials
        self.private_key = private_key

    def get_post_data(self):
        return json.dumps(
            {
                "uri": {
                    "absoluteUrl": self.uri.absolute_url,
                    "port": self.uri.port
                },
                "paths": self.paths,
                "credentials": {
                    "userName": self.credentials.username,
                    "password": self.credentials.password
                },
                "privateKey": self.private_key
            }
        )
