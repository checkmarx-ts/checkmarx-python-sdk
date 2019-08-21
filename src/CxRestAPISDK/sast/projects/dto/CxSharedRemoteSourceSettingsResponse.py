# encoding: utf-8


class CxSharedRemoteSourceSettingsResponse(object):
    def __init__(self, paths, link):
        """

        :param paths:  list of str
        :param link: CxLink
        """
        self.paths = paths
        self.link = link
