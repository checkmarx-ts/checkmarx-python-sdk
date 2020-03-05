# encoding: utf-8


class CxSharedRemoteSourceSettingsResponse(object):
    def __init__(self, paths, link):
        """

        Args:
            paths (:obj:`list` of :obj:`str`):
            link (:obj:`CxLink`):
        """
        self.paths = paths
        self.link = link

    def __str__(self):
        return "CxSharedRemoteSourceSettingsResponse(paths={}, link={})".format(
            self.paths, self.link
        )
